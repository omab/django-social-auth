"""
Base backends structures.

This module defines base classes needed to define custom OpenID or OAuth
auth services from third parties. This customs must subclass an Auth and
and Backend class, check current implementation for examples.

Also the modules *must* define a BACKENDS dictionary with the backend name
(which is used for URLs matching) and Auth class, otherwise it won't be
enabled.
"""
import logging
logger = logging.getLogger(__name__)

from os import walk
from os.path import basename
from urllib2 import Request, urlopen
from urllib import urlencode
from urlparse import urlsplit

from openid.consumer.consumer import Consumer, SUCCESS, CANCEL, FAILURE
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax

from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.utils import simplejson
from django.utils.importlib import import_module

from social_auth.models import UserSocialAuth
from social_auth.utils import setting
from social_auth.store import DjangoOpenIDStore
from social_auth.backends.exceptions import StopPipeline


# OpenID configuration
OLD_AX_ATTRS = [
    ('http://schema.openid.net/contact/email', 'old_email'),
    ('http://schema.openid.net/namePerson', 'old_fullname'),
    ('http://schema.openid.net/namePerson/friendly', 'old_nickname')
]
AX_SCHEMA_ATTRS = [
    # Request both the full name and first/last components since some
    # providers offer one but not the other.
    ('http://axschema.org/contact/email', 'email'),
    ('http://axschema.org/namePerson', 'fullname'),
    ('http://axschema.org/namePerson/first', 'first_name'),
    ('http://axschema.org/namePerson/last', 'last_name'),
    ('http://axschema.org/namePerson/friendly', 'nickname'),
]
SREG_ATTR = [
    ('email', 'email'),
    ('fullname', 'fullname'),
    ('nickname', 'nickname')
]
OPENID_ID_FIELD = 'openid_identifier'
SESSION_NAME = 'openid'

# key for username in user details dict used around, see get_user_details
# method
USERNAME = 'username'

PIPELINE = setting('SOCIAL_AUTH_PIPELINE', (
                'social_auth.backends.pipeline.social.social_auth_user',
                'social_auth.backends.pipeline.associate.associate_by_email',
                'social_auth.backends.pipeline.user.get_username',
                'social_auth.backends.pipeline.user.create_user',
                'social_auth.backends.pipeline.social.associate_user',
                'social_auth.backends.pipeline.social.load_extra_data',
                'social_auth.backends.pipeline.user.update_user_details',
           ))


class SocialAuthBackend(ModelBackend):
    """A django.contrib.auth backend that authenticates the user based on
    a authentication provider response"""
    name = ''  # provider name, it's stored in database

    def authenticate(self, *args, **kwargs):
        """Authenticate user using social credentials

        Authentication is made if this is the correct backend, backend
        verification is made by kwargs inspection for current backend
        name presence.
        """
        # Validate backend and arguments. Require that the Social Auth
        # response be passed in as a keyword argument, to make sure we
        # don't match the username/password calling conventions of
        # authenticate.
        if not (self.name and kwargs.get(self.name) and 'response' in kwargs):
            return None

        response = kwargs.get('response')
        details = self.get_user_details(response)
        uid = self.get_user_id(details, response)
        user = kwargs.get('user')
        request = kwargs.get('request')

        # Pipeline:
        #   Arguments:
        #       request, backend, social_user, uid, response, details
        #       user, is_new, args, kwargs
        kwargs = kwargs.copy()
        kwargs.update({
            'backend': self,
            'request': request,
            'uid': uid,
            'user': user,
            'social_user': None,
            'response': response,
            'details': details,
            'is_new': False,
        })
        for name in PIPELINE:
            mod_name, func_name = name.rsplit('.', 1)
            try:
                mod = import_module(mod_name)
            except ImportError:
                logger.exception('Error importing pipeline %s', name)
            else:
                pipeline = getattr(mod, func_name, None)
                if callable(pipeline):
                    try:
                        kwargs.update(pipeline(*args, **kwargs) or {})
                    except StopPipeline:
                        break

        social_user = kwargs.get('social_user')
        if social_user:
            # define user.social_user attribute to track current social
            # account
            user = social_user.user
            user.social_user = social_user
            return user

    def extra_data(self, user, uid, response, details):
        """Return default blank user extra data"""
        return ''

    def get_user_id(self, details, response):
        """Must return a unique ID from values returned on details"""
        raise NotImplementedError('Implement in subclass')

    def get_user_details(self, response):
        """Must return user details in a know internal struct:
            {USERNAME: <username if any>,
             'email': <user email if any>,
             'fullname': <user full name if any>,
             'first_name': <user first name if any>,
             'last_name': <user last name if any>}
        """
        raise NotImplementedError('Implement in subclass')


class OAuthBackend(SocialAuthBackend):
    """OAuth authentication backend base class.

    EXTRA_DATA defines a set of name that will be stored in
               extra_data field. It must be a list of tuples with
               name and alias.

    Also settings will be inspected to get more values names that should be
    stored on extra_data field. Setting name is created from current backend
    name (all uppercase) plus _EXTRA_DATA.

    access_token is always stored.
    """
    EXTRA_DATA = None

    def get_user_id(self, details, response):
        "OAuth providers return an unique user id in response"""
        return response['id']

    def extra_data(self, user, uid, response, details):
        """Return access_token and extra defined names to store in
        extra_data field"""
        data = {'access_token': response.get('access_token', '')}
        name = self.name.replace('-', '_').upper()
        names = (self.EXTRA_DATA or []) + setting(name + '_EXTRA_DATA', [])
        data.update((alias, response.get(name)) for name, alias in names)
        return data


class OpenIDBackend(SocialAuthBackend):
    """Generic OpenID authentication backend"""
    name = 'openid'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return response.identity_url

    def values_from_response(self, response, sreg_names=None, ax_names=None):
        """Return values from SimpleRegistration response or
        AttributeExchange response if present.

        @sreg_names and @ax_names must be a list of name and aliases
        for such name. The alias will be used as mapping key.
        """
        values = {}

        # Use Simple Registration attributes if provided
        if sreg_names:
            resp = sreg.SRegResponse.fromSuccessResponse(response)
            if resp:
                values.update((alias, resp.get(name) or '')
                                    for name, alias in sreg_names)

        # Use Attribute Exchange attributes if provided
        if ax_names:
            resp = ax.FetchResponse.fromSuccessResponse(response)
            if resp:
                for src, alias in ax_names:
                    name = alias.replace('old_', '')
                    values[name] = resp.getSingle(src, '') or values.get(name)
        return values

    def get_user_details(self, response):
        """Return user details from an OpenID request"""
        values = {USERNAME: '', 'email': '', 'fullname': '',
                  'first_name': '', 'last_name': ''}
        # update values using SimpleRegistration or AttributeExchange
        # values
        values.update(self.values_from_response(response,
                                                SREG_ATTR,
                                                OLD_AX_ATTRS + \
                                                AX_SCHEMA_ATTRS))

        fullname = values.get('fullname') or ''
        first_name = values.get('first_name') or ''
        last_name = values.get('last_name') or ''

        if not fullname and first_name and last_name:
            fullname = first_name + ' ' + last_name
        elif fullname:
            try:  # Try to split name for django user storage
                first_name, last_name = fullname.rsplit(' ', 1)
            except ValueError:
                last_name = fullname

        values.update({'fullname': fullname, 'first_name': first_name,
                       'last_name': last_name,
                       USERNAME: values.get(USERNAME) or \
                                   (first_name.title() + last_name.title())})
        return values

    def extra_data(self, user, uid, response, details):
        """Return defined extra data names to store in extra_data field.
        Settings will be inspected to get more values names that should be
        stored on extra_data field. Setting name is created from current
        backend name (all uppercase) plus _SREG_EXTRA_DATA and
        _AX_EXTRA_DATA because values can be returned by SimpleRegistration
        or AttributeExchange schemas.

        Both list must be a value name and an alias mapping similar to
        SREG_ATTR, OLD_AX_ATTRS or AX_SCHEMA_ATTRS
        """
        name = self.name.replace('-', '_').upper()
        sreg_names = setting(name + '_SREG_EXTRA_DATA')
        ax_names = setting(name + '_AX_EXTRA_DATA')
        data = self.values_from_response(response, sreg_names, ax_names)
        return data


class BaseAuth(object):
    """Base authentication class, new authenticators should subclass
    and implement needed methods.

        @AUTH_BACKEND   Authorization backend related with this service
    """
    AUTH_BACKEND = None

    def __init__(self, request, redirect):
        self.request = request
        # Use request because some auth providers use POST urls with needed
        # GET parameters on it
        self.data = request.REQUEST
        self.redirect = redirect

    def auth_url(self):
        """Must return redirect URL to auth provider"""
        raise NotImplementedError('Implement in subclass')

    def auth_html(self):
        """Must return login HTML content returned by provider"""
        raise NotImplementedError('Implement in subclass')

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        raise NotImplementedError('Implement in subclass')

    def auth_extra_arguments(self):
        """Return extra argumens needed on auth process, setting is per bancked
        and defined by <backend name in uppercase>_AUTH_EXTRA_ARGUMENTS.
        """
        name = self.AUTH_BACKEND.name.upper() + '_AUTH_EXTRA_ARGUMENTS'
        return getattr(settings, name, {})

    @property
    def uses_redirect(self):
        """Return True if this provider uses redirect url method,
        otherwise return false."""
        return True

    @classmethod
    def enabled(cls):
        """Return backend enabled status, all enabled by default"""
        return True

    def disconnect(self, user, association_id=None):
        """Deletes current backend from user if associated.
        Override if extra operations are needed.
        """
        if association_id:
            user.social_auth.get(id=association_id).delete()
        else:
            user.social_auth.filter(provider=self.AUTH_BACKEND.name).delete()


class OpenIdAuth(BaseAuth):
    """OpenId process handling"""
    AUTH_BACKEND = OpenIDBackend

    def auth_url(self):
        """Return auth URL returned by service"""
        openid_request = self.setup_request(self.auth_extra_arguments())
        # Construct completion URL, including page we should redirect to
        return_to = self.request.build_absolute_uri(self.redirect)
        return openid_request.redirectURL(self.trust_root(), return_to)

    def auth_html(self):
        """Return auth HTML returned by service"""
        openid_request = self.setup_request(self.auth_extra_arguments())
        return_to = self.request.build_absolute_uri(self.redirect)
        form_tag = {'id': 'openid_message'}
        return openid_request.htmlMarkup(self.trust_root(), return_to,
                                         form_tag_attrs=form_tag)

    def trust_root(self):
        """Return trust-root option"""
        return setting('OPENID_TRUST_ROOT') or \
               self.request.build_absolute_uri('/')

    def auth_complete(self, *args, **kwargs):
        """Complete auth process"""
        response = self.consumer().complete(dict(self.data.items()),
                                            self.request.build_absolute_uri())
        if not response:
            raise ValueError('This is an OpenID relying party endpoint')
        elif response.status == SUCCESS:
            kwargs.update({'response': response, self.AUTH_BACKEND.name: True})
            return authenticate(*args, **kwargs)
        elif response.status == FAILURE:
            raise ValueError('OpenID authentication failed: %s' % \
                             response.message)
        elif response.status == CANCEL:
            raise ValueError('Authentication cancelled')
        else:
            raise ValueError('Unknown OpenID response type: %r' % \
                             response.status)

    def setup_request(self, extra_params=None):
        """Setup request"""
        openid_request = self.openid_request(extra_params)
        # Request some user details. Use attribute exchange if provider
        # advertises support.
        if openid_request.endpoint.supportsType(ax.AXMessage.ns_uri):
            fetch_request = ax.FetchRequest()
            # Mark all attributes as required, Google ignores optional ones
            for attr, alias in (AX_SCHEMA_ATTRS + OLD_AX_ATTRS):
                fetch_request.add(ax.AttrInfo(attr, alias=alias,
                                              required=True))
        else:
            fetch_request = sreg.SRegRequest(optional=dict(SREG_ATTR).keys())
        openid_request.addExtension(fetch_request)

        return openid_request

    def consumer(self):
        """Create an OpenID Consumer object for the given Django request."""
        return Consumer(self.request.session.setdefault(SESSION_NAME, {}),
                        DjangoOpenIDStore())

    @property
    def uses_redirect(self):
        """Return true if openid request will be handled with redirect or
        HTML content will be returned.
        """
        return self.openid_request().shouldSendRedirect()

    def openid_request(self, extra_params=None):
        """Return openid request"""
        openid_url = self.openid_url()
        if extra_params:
            query = urlsplit(openid_url).query
            openid_url += (query and '&' or '?') + urlencode(extra_params)

        try:
            return self.consumer().begin(openid_url)
        except DiscoveryFailure, err:
            raise ValueError('OpenID discovery error: %s' % err)

    def openid_url(self):
        """Return service provider URL.
        This base class is generic accepting a POST parameter that specifies
        provider URL."""
        if OPENID_ID_FIELD not in self.data:
            raise ValueError('Missing openid identifier')
        return self.data[OPENID_ID_FIELD]


class BaseOAuth(BaseAuth):
    """OAuth base class"""
    def __init__(self, request, redirect):
        """Init method"""
        super(BaseOAuth, self).__init__(request, redirect)
        self.redirect_uri = self.request.build_absolute_uri(self.redirect)


class ConsumerBasedOAuth(BaseOAuth):
    """Consumer based mechanism OAuth authentication, fill the needed
    parameters to communicate properly with authentication service.

        @AUTHORIZATION_URL       Authorization service url
        @REQUEST_TOKEN_URL       Request token URL
        @ACCESS_TOKEN_URL        Access token URL
        @SERVER_URL              Authorization server URL
    """
    AUTHORIZATION_URL = ''
    REQUEST_TOKEN_URL = ''
    ACCESS_TOKEN_URL = ''
    SERVER_URL = ''
    SETTINGS_KEY_NAME = ''
    SETTINGS_SECRET_NAME = ''

    def auth_url(self):
        """Return redirect url"""
        token = self.unauthorized_token()
        name = self.AUTH_BACKEND.name + 'unauthorized_token_name'
        self.request.session[name] = token.to_string()
        return self.oauth_request(token, self.AUTHORIZATION_URL,
                                  self.auth_extra_arguments()).to_url()

    def auth_complete(self, *args, **kwargs):
        """Return user, might be logged in"""
        name = self.AUTH_BACKEND.name + 'unauthorized_token_name'
        unauthed_token = self.request.session.get(name)
        if not unauthed_token:
            raise ValueError('Missing unauthorized token')

        token = Token.from_string(unauthed_token)
        if token.key != self.data.get('oauth_token', 'no-token'):
            raise ValueError('Incorrect tokens')

        access_token = self.access_token(token)
        data = self.user_data(access_token)
        if data is not None:
            data['access_token'] = access_token.to_string()

        kwargs.update({'response': data, self.AUTH_BACKEND.name: True})
        return authenticate(*args, **kwargs)

    def unauthorized_token(self):
        """Return request for unauthorized token (first stage)"""
        request = self.oauth_request(token=None, url=self.REQUEST_TOKEN_URL)
        response = self.fetch_response(request)
        return Token.from_string(response)

    def oauth_request(self, token, url, extra_params=None):
        """Generate OAuth request, setups callback url"""
        params = {'oauth_callback': self.redirect_uri}
        if extra_params:
            params.update(extra_params)

        if 'oauth_verifier' in self.data:
            params['oauth_verifier'] = self.data['oauth_verifier']
        request = OAuthRequest.from_consumer_and_token(self.consumer,
                                                       token=token,
                                                       http_url=url,
                                                       parameters=params)
        request.sign_request(SignatureMethod_HMAC_SHA1(), self.consumer, token)
        return request

    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        response = urlopen(request.to_url())
        return '\n'.join(response.readlines())

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        return Token.from_string(self.fetch_response(request))

    def user_data(self, access_token):
        """Loads user data from service"""
        raise NotImplementedError('Implement in subclass')

    @property
    def consumer(self):
        """Setups consumer"""
        return OAuthConsumer(*self.get_key_and_secret())

    def get_key_and_secret(self):
        """Return tuple with Consumer Key and Consumer Secret for current
        service provider. Must return (key, secret), order *must* be respected.
        """
        return setting(self.SETTINGS_KEY_NAME), \
               setting(self.SETTINGS_SECRET_NAME)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in
                        (cls.SETTINGS_KEY_NAME, cls.SETTINGS_SECRET_NAME))


class BaseOAuth2(BaseOAuth):
    """Base class for OAuth2 providers.

    OAuth2 draft details at:
        http://tools.ietf.org/html/draft-ietf-oauth-v2-10

    Attributes:
        @AUTHORIZATION_URL       Authorization service url
        @ACCESS_TOKEN_URL        Token URL
    """
    AUTHORIZATION_URL = None
    ACCESS_TOKEN_URL = None
    SCOPE_SEPARATOR = ' '
    RESPONSE_TYPE = 'code'

    def auth_url(self):
        """Return redirect url"""
        client_id, client_secret = self.get_key_and_secret()
        args = {'client_id': client_id, 'redirect_uri': self.redirect_uri}

        scope = self.get_scope()
        if scope:
            args['scope'] = self.SCOPE_SEPARATOR.join(self.get_scope())
        if self.RESPONSE_TYPE:
            args['response_type'] = self.RESPONSE_TYPE

        args.update(self.auth_extra_arguments())
        return self.AUTHORIZATION_URL + '?' + urlencode(args)

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if self.data.get('error'):
            error = self.data.get('error_description') or self.data['error']
            raise ValueError('OAuth2 authentication failed: %s' % error)

        client_id, client_secret = self.get_key_and_secret()
        params = {'grant_type': 'authorization_code',  # request auth code
                  'code': self.data.get('code', ''),  # server response code
                  'client_id': client_id,
                  'client_secret': client_secret,
                  'redirect_uri': self.redirect_uri}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=headers)

        try:
            response = simplejson.loads(urlopen(request).read())
        except (ValueError, KeyError):
            raise ValueError('Unknown OAuth2 response type')

        if response.get('error'):
            error = response.get('error_description') or response.get('error')
            raise ValueError('OAuth2 authentication failed: %s' % error)
        else:
            response.update(self.user_data(response['access_token']) or {})
            kwargs.update({'response': response, self.AUTH_BACKEND.name: True})
            return authenticate(*args, **kwargs)

    def get_scope(self):
        """Return list with needed access scope"""
        return []

    def get_key_and_secret(self):
        """Return tuple with Consumer Key and Consumer Secret for current
        service provider. Must return (key, secret), order *must* be respected.
        """
        return setting(self.SETTINGS_KEY_NAME), \
               setting(self.SETTINGS_SECRET_NAME)


# import sources from where check for auth backends
SOCIAL_AUTH_IMPORT_SOURCES = (
    'social_auth.backends',
    'social_auth.backends.contrib',
) + setting('SOCIAL_AUTH_IMPORT_BACKENDS', ())

def get_backends():
    backends = {}
    enabled_backends = setting('SOCIAL_AUTH_ENABLED_BACKENDS')

    for mod_name in SOCIAL_AUTH_IMPORT_SOURCES:
        try:
            mod = import_module(mod_name)
        except ImportError:
            logger.exception('Error importing %s', mod_name)
            continue

        for directory, subdir, files in walk(mod.__path__[0]):
            for name in filter(lambda name: name.endswith('.py'), files):
                try:
                    name = basename(name).replace('.py', '')
                    sub = import_module(mod_name + '.' + name)
                    # register only enabled backends
                    backends.update(((key, val)
                                        for key, val in sub.BACKENDS.items()
                                            if val.enabled() and
                                               (not enabled_backends or
                                                key in enabled_backends)))
                except (ImportError, AttributeError):
                    pass
    return backends

# load backends from defined modules
BACKENDS = get_backends()
BACKENDS[OpenIdAuth.AUTH_BACKEND.name] = OpenIdAuth

def get_backend(name, *args, **kwargs):
    """Return auth backend instance *if* it's registered, None in other case"""
    return BACKENDS.get(name, lambda *args, **kwargs: None)(*args, **kwargs)

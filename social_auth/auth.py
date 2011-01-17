"""Authentication handling class"""
import cgi
import urllib
import urllib2
import httplib

from openid.consumer.consumer import Consumer, SUCCESS, CANCEL, FAILURE
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax
from oauth.oauth import OAuthConsumer, OAuthToken, OAuthRequest, \
                        OAuthSignatureMethod_HMAC_SHA1

from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from .store import DjangoOpenIDStore
from .backends import TwitterBackend, OrkutBackend, FacebookBackend, \
                      OpenIDBackend, GoogleBackend, YahooBackend, \
                      GoogleOAuthBackend, LiveJournalBackend
from .conf import AX_ATTRS, SREG_ATTR, OPENID_ID_FIELD, SESSION_NAME, \
                  OPENID_GOOGLE_URL, OPENID_YAHOO_URL, TWITTER_SERVER, \
                  OPENID_LIVEJOURNAL_URL, OPENID_LIVEJOURNAL_USER_FIELD, \
                  TWITTER_REQUEST_TOKEN_URL, TWITTER_ACCESS_TOKEN_URL, \
                  TWITTER_AUTHORIZATION_URL, TWITTER_CHECK_AUTH, \
                  FACEBOOK_CHECK_AUTH, FACEBOOK_AUTHORIZATION_URL, \
                  FACEBOOK_ACCESS_TOKEN_URL, GOOGLE_REQUEST_TOKEN_URL, \
                  GOOGLE_ACCESS_TOKEN_URL, GOOGLE_AUTHORIZATION_URL, \
                  GOOGLE_SERVER, GOOGLE_OAUTH_SCOPE, GOOGLEAPIS_EMAIL, \
                  ORKUT_REST_ENDPOINT, ORKUT_DEFAULT_DATA, ORKUT_SCOPE


class BaseAuth(object):
    """Base authentication class, new authenticators should subclass
    and implement needed methods"""
    def __init__(self, request, redirect):
        self.request = request
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

    @property
    def uses_redirect(self):
        """Return True if this provider uses redirect url method,
        otherwise return false."""
        return True


class OpenIdAuth(BaseAuth):
    """
    OpenId process handling
        @AUTH_BACKEND   Authorization backend related with this service
    """
    AUTH_BACKEND = OpenIDBackend

    def auth_url(self):
        openid_request = self.setup_request()
        # Construct completion URL, including page we should redirect to
        return_to = self.request.build_absolute_uri(self.redirect)
        trust_root = getattr(settings, 'OPENID_TRUST_ROOT',
                             self.request.build_absolute_uri('/'))
        return openid_request.redirectURL(trust_root, return_to)

    def auth_html(self):
        openid_request = self.setup_request()
        return_to = self.request.build_absolute_uri(self.redirect)
        trust_root = getattr(settings, 'OPENID_TRUST_ROOT',
                             self.request.build_absolute_uri('/'))
        form_tag = {'id': 'openid_message'}
        return openid_request.htmlMarkup(trust_root, return_to,
                                         form_tag_attrs=form_tag)

    def auth_complete(self, *args, **kwargs):
        response = self.consumer().complete(dict(self.request.REQUEST.items()),
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

    def setup_request(self):
        """Setup request"""
        openid_request = self.openid_request()
        # Request some user details. Use attribute exchange if provider
        # advertises support.
        if openid_request.endpoint.supportsType(ax.AXMessage.ns_uri):
            fetch_request = ax.FetchRequest()
            # Mark all attributes as required, Google ignores optional ones
            for attr, alias in AX_ATTRS:
                fetch_request.add(ax.AttrInfo(attr, alias=alias,
                                              required=True))
        else:
            fetch_request = sreg.SRegRequest(optional=SREG_ATTR)
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
        if not hasattr(self, '_uses_redirect'):
            setattr(self, '_uses_redirect',
                    self.openid_request().shouldSendRedirect())
        return getattr(self, '_uses_redirect', True)

    def openid_request(self):
        """Return openid request"""
        if not hasattr(self, '_openid_request'):
            openid_url = self.openid_url()
            try:
                openid_request = self.consumer().begin(openid_url)
            except DiscoveryFailure, err:
                raise ValueError('OpenID discovery error: %s' % err)
            else:
                setattr(self, '_openid_request', openid_request)
        return getattr(self, '_openid_request', None)

    def openid_url(self):
        """Return service provider URL.
        This base class is generic accepting a POST parameter that specifies
        provider URL."""
        if self.request.method != 'POST' or \
           OPENID_ID_FIELD not in self.request.POST:
            raise ValueError('Missing openid identifier')
        return self.request.POST[OPENID_ID_FIELD]


class GoogleAuth(OpenIdAuth):
    """Google OpenID authentication"""
    AUTH_BACKEND = GoogleBackend

    def openid_url(self):
        """Return Google OpenID service url"""
        return OPENID_GOOGLE_URL


class YahooAuth(OpenIdAuth):
    """Yahoo OpenID authentication"""
    AUTH_BACKEND = YahooBackend

    def openid_url(self):
        """Return Yahoo OpenID service url"""
        return OPENID_YAHOO_URL


class LiveJournalAuth(OpenIdAuth):
    """LiveJournal OpenID authentication"""
    AUTH_BACKEND = LiveJournalBackend

    def uses_redirect(self):
        """LiveJournal uses redirect"""
        return True

    def openid_url(self):
        """Returns LiveJournal authentication URL"""
        if self.request.method != 'POST' or \
           not self.request.POST.get(OPENID_LIVEJOURNAL_USER_FIELD):
            raise ValueError, 'Missing LiveJournal user identifier'
        return OPENID_LIVEJOURNAL_URL % \
                    self.request.POST[OPENID_LIVEJOURNAL_USER_FIELD]


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
        @AUTH_BACKEND            Authorization backend related with
                                 this service
    """
    AUTHORIZATION_URL = ''
    REQUEST_TOKEN_URL = ''
    ACCESS_TOKEN_URL = ''
    SERVER_URL = ''
    AUTH_BACKEND = None

    def auth_url(self):
        """Returns redirect url"""
        token = self.unauthorized_token()
        name = self.AUTH_BACKEND.name + 'unauthorized_token_name'
        self.request.session[name] = token.to_string()
        return self.oauth_request(token, self.AUTHORIZATION_URL).to_url()

    def auth_complete(self, *args, **kwargs):
        """Returns user, might be logged in"""
        name = self.AUTH_BACKEND.name + 'unauthorized_token_name'
        unauthed_token = self.request.session.get(name)
        if not unauthed_token:
            raise ValueError('Missing unauthorized token')

        token = OAuthToken.from_string(unauthed_token)
        if token.key != self.request.GET.get('oauth_token', 'no-token'):
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
        return OAuthToken.from_string(response)

    def oauth_request(self, token, url, extra_params=None):
        """Generate OAuth request, setups callback url"""
        params = {'oauth_callback': self.redirect_uri}
        if extra_params:
            params.update(extra_params)

        if 'oauth_verifier' in self.request.GET:
            params['oauth_verifier'] = self.request.GET['oauth_verifier']
        request = OAuthRequest.from_consumer_and_token(self.consumer,
                                                       token=token,
                                                       http_url=url,
                                                       parameters=params)
        request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), self.consumer,
                             token)
        return request

    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        self.connection.request(request.http_method, request.to_url())
        response = self.connection.getresponse()
        return response.read()

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        return OAuthToken.from_string(self.fetch_response(request))

    def user_data(self, access_token):
        """Loads user data from service"""
        raise NotImplementedError('Implement in subclass')

    @property
    def connection(self):
        """Setups connection"""
        conn = getattr(self, '_connection', None)
        if conn is None:
            conn = httplib.HTTPSConnection(self.SERVER_URL)
            setattr(self, '_connection', conn)
        return conn

    @property
    def consumer(self):
        """Setups consumer"""
        cons = getattr(self, '_consumer', None)
        if cons is None:
            cons = OAuthConsumer(*self.get_key_and_secret())
            setattr(self, '_consumer', cons)
        return cons

    def get_key_and_secret(self):
        """Return tuple with Consumer Key and Consumer Secret for current
        service provider. Must return (key, secret), order must be respected.
        """
        raise NotImplementedError('Implement in subclass')


class BaseGoogleOAuth(ConsumerBasedOAuth):
    """Base class for Google OAuth mechanism"""
    AUTHORIZATION_URL = GOOGLE_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = GOOGLE_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = GOOGLE_ACCESS_TOKEN_URL
    SERVER_URL = GOOGLE_SERVER
    AUTH_BACKEND = None

    def user_data(self, access_token):
        """Loads user data from G service"""
        raise NotImplementedError('Implement in subclass')

    def get_key_and_secret(self):
        """Return Consumer Key and Consumer Secret pair"""
        raise NotImplementedError('Implement in subclass')


class OrkutAuth(BaseGoogleOAuth):
    """Orkut OAuth authentication mechanism"""
    AUTH_BACKEND = OrkutBackend

    def user_data(self, access_token):
        """Loads user data from Orkut service"""
        fields = ORKUT_DEFAULT_DATA
        if hasattr(settings, 'ORKUT_EXTRA_DATA'):
            fields += ',' + settings.ORKUT_EXTRA_DATA
        scope = ORKUT_SCOPE + \
                getattr(settings, 'ORKUT_EXTRA_SCOPE', [])
        params = {'method': 'people.get',
                  'id': 'myself',
                  'userId': '@me',
                  'groupId': '@self',
                  'fields': fields,
                  'scope': ' '.join(scope)}
        request = self.oauth_request(access_token, ORKUT_REST_ENDPOINT, params)
        response = urllib.urlopen(request.to_url()).read()
        try:
            return simplejson.loads(response)['data']
        except (simplejson.JSONDecodeError, KeyError):
            return None

    def get_key_and_secret(self):
        """Return Orkut Consumer Key and Consumer Secret pair"""
        return settings.ORKUT_CONSUMER_KEY, settings.ORKUT_CONSUMER_SECRET


class GoogleOAuth(BaseGoogleOAuth):
    """Google OAuth authorization mechanism"""
    AUTH_BACKEND = GoogleOAuthBackend

    def user_data(self, access_token):
        """Loads user data data from googleapis service, only email so far
        as it's described in:
            http://sites.google.com/site/oauthgoog/Home/emaildisplayscope
        OAuth parameters needs to be passed in the queryset and
        Authorization header, this behavior is listed in:
            http://groups.google.com/group/oauth/browse_thread/thread/d15add9beb418ebc
        """
        url = self.oauth_request(access_token, GOOGLEAPIS_EMAIL,
                                 {'alt': 'json'}).to_url()
        params = url.split('?', 1)[1]
        request = urllib2.Request(url)
        request.headers['Authorization'] = params # setup header
        response = urllib2.urlopen(request).read()
        try:
            return simplejson.loads(response)['data']
        except (simplejson.JSONDecodeError, KeyError):
            return None

    def oauth_request(self, token, url, extra_params=None):
        extra_params = extra_params or {}
        scope = GOOGLE_OAUTH_SCOPE + \
                getattr(settings, 'GOOGLE_OAUTH_EXTRA_SCOPE', [])
        extra_params.update({
            'scope': ' '.join(scope),
            'xoauth_displayname': getattr(settings, 'GOOGLE_DISPLAY_NAME',
                                          'Social Auth')
        })
        return super(GoogleOAuth, self).oauth_request(token, url, extra_params)

    def get_key_and_secret(self):
        """Return Google OAuth Consumer Key and Consumer Secret pair, uses
        anonymous by default, beware that this marks the application as not
        registered and a security badge is displayed on authorization page.
        http://code.google.com/apis/accounts/docs/OAuth_ref.html#SigningOAuth
        """
        return getattr(settings, 'GOOGLE_CONSUMER_KEY', 'anonymous'), \
               getattr(settings, 'GOOGLE_CONSUMER_SECRET', 'anonymous')


class TwitterAuth(ConsumerBasedOAuth):
    """Twitter OAuth authentication mechanism"""
    AUTHORIZATION_URL = TWITTER_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = TWITTER_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = TWITTER_ACCESS_TOKEN_URL
    SERVER_URL = TWITTER_SERVER
    AUTH_BACKEND = TwitterBackend

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, TWITTER_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except simplejson.JSONDecodeError:
            return None

    def get_key_and_secret(self):
        """Return Twitter Consumer Key and Consumer Secret pair"""
        return settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET


class FacebookAuth(BaseOAuth):
    """Facebook OAuth mechanism"""

    def auth_url(self):
        """Returns redirect url"""
        args = {'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': self.redirect_uri}
        if hasattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS'):
            args['scope'] = ','.join(settings.FACEBOOK_EXTENDED_PERMISSIONS)
        return FACEBOOK_AUTHORIZATION_URL + '?' + urllib.urlencode(args)

    def auth_complete(self, *args, **kwargs):
        """Returns user, might be logged in"""
        if 'code' in self.request.GET:
            url = FACEBOOK_ACCESS_TOKEN_URL + '?' + \
                  urllib.urlencode({'client_id': settings.FACEBOOK_APP_ID,
                                'redirect_uri': self.redirect_uri,
                                'client_secret': settings.FACEBOOK_API_SECRET,
                                'code': self.request.GET['code']})
            response = cgi.parse_qs(urllib.urlopen(url).read())

            access_token = response['access_token'][0]
            data = self.user_data(access_token)
            if data is not None:
                if 'error' in data:
                    raise ValueError('Authentication error')
                data['access_token'] = access_token

            kwargs.update({'response': data, FacebookBackend.name: True})
            return authenticate(*args, **kwargs)
        else:
            raise ValueError('Authentication error')

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'access_token': access_token}
        url = FACEBOOK_CHECK_AUTH + '?' + urllib.urlencode(params)
        try:
            return simplejson.load(urllib.urlopen(url))
        except simplejson.JSONDecodeError:
            return None


# Authentication backends
BACKENDS = {
    'twitter': TwitterAuth,
    'facebook': FacebookAuth,
    'google': GoogleAuth,
    'google-oauth': GoogleOAuth,
    'yahoo': YahooAuth,
    'livejournal': LiveJournalAuth,
    'orkut': OrkutAuth,
    'openid': OpenIdAuth,
}

def get_backend(name, *args, **kwargs):
    """Return auth backend instance *if* it's registered, None in other case"""
    return BACKENDS.get(name, lambda *args, **kwargs: None)(*args, **kwargs)

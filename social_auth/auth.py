"""Authentication handling class"""
import cgi
import urllib
import httplib

from openid.consumer.consumer import Consumer, SUCCESS, CANCEL, FAILURE
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax
from oauth.oauth import OAuthConsumer, OAuthToken, OAuthRequest, \
                        OAuthSignatureMethod_HMAC_SHA1

from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from .base import BaseAuth
from .store import DjangoOpenIDStore
from .conf import AX_ATTRS, SREG_ATTR, OPENID_ID_FIELD, SESSION_NAME, \
                  OPENID_GOOGLE_URL, OPENID_YAHOO_URL, TWITTER_SERVER, \
                  TWITTER_REQUEST_TOKEN_URL, TWITTER_ACCESS_TOKEN_URL, \
                  TWITTER_AUTHORIZATION_URL, TWITTER_CHECK_AUTH, \
                  TWITTER_UNAUTHORIZED_TOKEN_NAME, FACEBOOK_CHECK_AUTH, \
                  FACEBOOK_AUTHORIZATION_URL, FACEBOOK_ACCESS_TOKEN_URL, \
                  ORKUT_SERVER, ORKUT_SCOPE, ORKUT_UNAUTHORIZED_TOKEN_NAME, \
                  ORKUT_REQUEST_TOKEN_URL, ORKUT_ACCESS_TOKEN_URL, \
                  ORKUT_AUTHORIZATION_URL, ORKUT_REST_ENDPOINT, ORKUT_EXTRA_DATA


class OpenIdAuth(BaseAuth):
    """OpenId process handling"""
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

    def auth_complete(self):
        response = self.consumer().complete(dict(self.request.REQUEST.items()),
                                            self.request.build_absolute_uri())
        if not response:
            raise ValueError, 'This is an OpenID relying party endpoint'
        elif response.status == SUCCESS:
            return authenticate(response=response, openid=True)
        elif response.status == FAILURE:
            raise ValueError, 'OpenID authentication failed: %s' % response.message
        elif response.status == CANCEL:
            raise ValueError, 'Authentication cancelled'
        else:
            raise ValueError, 'Unknown OpenID response type: %r' % response.status

    def setup_request(self):
        """Setup request"""
        openid_request = self.openid_request()
        # Request some user details.  If the provider advertises support
        # for attribute exchange, use that.
        if openid_request.endpoint.supportsType(ax.AXMessage.ns_uri):
            fetch_request = ax.FetchRequest()
            # Mark all attributes as required, since Google ignores optional ones
            for attr, alias in AX_ATTRS:
                fetch_request.add(ax.AttrInfo(attr, alias=alias, required=True))
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
            setattr(self, '_uses_redirect', self.openid_request().shouldSendRedirect())
        return getattr(self, '_uses_redirect', True)

    def openid_request(self):
        """Return openid request"""
        if not hasattr(self, '_openid_request'):
            openid_url = self.openid_url()
            try:
                openid_request = self.consumer().begin(openid_url)
            except DiscoveryFailure, e:
                raise ValueError, 'OpenID discovery error: %s' % e
            else:
                setattr(self, '_openid_request', openid_request)
        return getattr(self, '_openid_request', None)

    def openid_url(self):
        """Return service provider URL.
        This base class is generic accepting a POST parameter that specifies
        provider URL."""
        if self.request.method != 'POST' or OPENID_ID_FIELD not in self.request.POST:
            raise ValueError, 'Missing openid identifier'
        return self.request.POST[OPENID_ID_FIELD]


class GoogleAuth(OpenIdAuth):
    """Google OpenID authentication"""
    def openid_url(self):
        """Return Google OpenID service url"""
        return OPENID_GOOGLE_URL


class YahooAuth(OpenIdAuth):
    """Yahoo OpenID authentication"""
    def openid_url(self):
        """Return Yahoo OpenID service url"""
        return OPENID_YAHOO_URL


class BaseOAuth(BaseAuth):
    """OAuth base class"""
    def __init__(self, request, redirect):
        """Init method"""
        super(BaseOAuth, self).__init__(request, redirect)
        self.redirect_uri = self.request.build_absolute_uri(self.redirect)


class OrkutAuth(BaseOAuth):
    """Orkut OAuth authentication mechanism"""
    def auth_url(self):
        """Returns redirect url"""
        token = self.unauthorized_token()
        self.request.session[ORKUT_UNAUTHORIZED_TOKEN_NAME] = token.to_string()
        return self.oauth_request(token, ORKUT_AUTHORIZATION_URL).to_url()

    def auth_complete(self):
        """Returns user, might be logged in"""
        unauthed_token = self.request.session.get(ORKUT_UNAUTHORIZED_TOKEN_NAME)
        if not unauthed_token:
            raise ValueError, 'Missing unauthorized token'

        token = OAuthToken.from_string(unauthed_token)
        if token.key != self.request.GET.get('oauth_token', 'no-token'):
            raise ValueError, 'Incorrect tokens'
        access_token = self.access_token(token)
        data = self.user_data(access_token)
        if data is not None:
            data['access_token'] = access_token.to_string()
        return authenticate(response=data, orkut=True)

    def unauthorized_token(self):
        """Return request for unauthorized token (first stage)"""
        request = self.oauth_request(token=None, url=ORKUT_REQUEST_TOKEN_URL)
        response = self.fetch_response(request)
        return OAuthToken.from_string(response)

    def oauth_request(self, token, url, params={}):
        """Generate OAuth request, setups callback url"""
        params.update({'oauth_callback': self.redirect_uri, \
                                'scope': ORKUT_SCOPE})
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
        request = self.oauth_request(token, ORKUT_ACCESS_TOKEN_URL)
        return OAuthToken.from_string(self.fetch_response(request))

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'method': 'people.get', \
                      'id': 'myself', \
                  'userId': '@me', \
                 'groupId': '@self', \
                  'fields': 'name,displayName,emails,%s' % ORKUT_EXTRA_DATA}
        request = self.oauth_request(access_token, ORKUT_REST_ENDPOINT, params)
        response = urllib.urlopen(request.to_url()).read()
        try:
            json = simplejson.loads(response)
            return json['data']
        except simplejson.JSONDecodeError:
            return None

    @property
    def connection(self):
        """Setups connection"""
        conn = getattr(self, '_connection', None)
        if conn is None:
            conn = httplib.HTTPSConnection(ORKUT_SERVER)
            setattr(self, '_connection', conn)
        return conn

    @property
    def consumer(self):
        """Setups consumer"""
        cons = getattr(self, '_consumer', None)
        if cons is None:
            cons = OAuthConsumer(settings.ORKUT_CONSUMER_KEY,
                                 settings.ORKUT_CONSUMER_SECRET)
            setattr(self, '_consumer', cons)
        return cons


class TwitterAuth(BaseOAuth):
    """Twitter OAuth authentication mechanism"""
    def auth_url(self):
        """Returns redirect url"""
        token = self.unauthorized_token()
        self.request.session[TWITTER_UNAUTHORIZED_TOKEN_NAME] = token.to_string()   
        return self.oauth_request(token, TWITTER_AUTHORIZATION_URL).to_url()

    def auth_complete(self):
        """Returns user, might be logged in"""
        unauthed_token = self.request.session.get(TWITTER_UNAUTHORIZED_TOKEN_NAME)
        if not unauthed_token:
            raise ValueError, 'Missing unauthorized token'

        token = OAuthToken.from_string(unauthed_token)   
        if token.key != self.request.GET.get('oauth_token', 'no-token'):
            raise ValueError, 'Incorrect tokens'
        access_token = self.access_token(token)
        data = self.user_data(access_token)
        if data is not None:
            data['access_token'] = access_token.to_string()
        return authenticate(response=data, twitter=True)

    def unauthorized_token(self):
        """Return request for unauthorized token (first stage)"""
        request = self.oauth_request(token=None, url=TWITTER_REQUEST_TOKEN_URL)
        response = self.fetch_response(request)
        return OAuthToken.from_string(response)

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, TWITTER_ACCESS_TOKEN_URL)
        return OAuthToken.from_string(self.fetch_response(request))

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, TWITTER_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except simplejson.JSONDecodeError:
            return None

    def oauth_request(self, token, url):
        """Generate OAuth request, setups callback url"""
        params = {'oauth_callback': self.redirect_uri}
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

    @property
    def connection(self):
        """Setups connection"""
        conn = getattr(self, '_connection', None)
        if conn is None:
            conn = httplib.HTTPSConnection(TWITTER_SERVER)
            setattr(self, '_connection', conn)
        return conn

    @property
    def consumer(self):
        """Setups consumer"""
        cons = getattr(self, '_consumer', None)
        if cons is None:
            cons = OAuthConsumer(settings.TWITTER_CONSUMER_KEY,
                                 settings.TWITTER_CONSUMER_SECRET)
            setattr(self, '_consumer', cons)
        return cons


class FacebookAuth(BaseOAuth):
    """Facebook OAuth mechanism"""
    def __init__(self, request, redirect):
        super(FacebookAuth, self).__init__(request, redirect)
        if settings.DEBUG and self.redirect_uri:
            # Facebook doesn't accept custom ports
            self.redirect_uri = self.redirect_uri.replace(':8000', '')

    def auth_url(self):
        """Returns redirect url"""
        args = {'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': self.redirect_uri}
        return FACEBOOK_AUTHORIZATION_URL + '?' + urllib.urlencode(args)

    def auth_complete(self):
        """Returns user, might be logged in"""
        if 'code' in self.request.GET:
            args = {'client_id': settings.FACEBOOK_APP_ID,
                    'redirect_uri': self.redirect_uri,
                    'client_secret': settings.FACEBOOK_API_SECRET,
                    'code': self.request.GET['code']}
            url = FACEBOOK_ACCESS_TOKEN_URL + '?' + urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
        
            access_token = response['access_token'][0]
            data = self.user_data(access_token)
            if data is not None:
                if 'error' in data:
                    raise ValueError, 'Authentication error'
                data['access_token'] = access_token
            return authenticate(response=data, facebook=True)
        else:
            raise ValueError, 'Authentication error'

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'access_token': access_token}
        url = FACEBOOK_CHECK_AUTH + '?' + urllib.urlencode(params)
        try:
            return simplejson.load(urllib.urlopen(url))
        except simplejson.JSONDecodeError:
            return None

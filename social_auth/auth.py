import cgi
import urllib
import httplib
from openid.consumer.consumer import Consumer, SUCCESS, CANCEL, FAILURE
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax

from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from .base import BaseAuth
from .store import DjangoOpenIDStore
from .oauth import OAuthConsumer, OAuthToken, OAuthRequest, \
                   OAuthSignatureMethod_HMAC_SHA1
from .conf import AX_ATTRS, SREG_ATTR, OPENID_ID_FIELD, SESSION_NAME, \
                  OPENID_GOOGLE_URL, OPENID_YAHOO_URL, TWITTER_SERVER, \
                  TWITTER_REQUEST_TOKEN_URL, TWITTER_ACCESS_TOKEN_URL, \
                  TWITTER_AUTHORIZATION_URL, TWITTER_CHECK_AUTH, \
                  TWITTER_UNAUTHORIZED_TOKEN_NAME, FACEBOOK_CHECK_AUTH, \
                  FACEBOOK_AUTHORIZATION_URL, FACEBOOK_ACCESS_TOKEN_URL


class OpenIdAuth(BaseAuth):
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
        if not hasattr(self, '_uses_redirect'):
            setattr(self, '_uses_redirect', self.openid_request().shouldSendRedirect())
        return getattr(self, '_uses_redirect', True)

    def openid_request(self):
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
        if self.request.method != 'POST' or OPENID_ID_FIELD not in self.request.POST:
            raise ValueError, 'Missing openid identifier'
        return self.request.POST[OPENID_ID_FIELD]


class GoogleAuth(OpenIdAuth):
    """Google OpenID authentication"""
    def openid_url(self):
        return OPENID_GOOGLE_URL


class YahooAuth(OpenIdAuth):
    """Yahoo OpenID authentication"""
    def openid_url(self):
        return OPENID_YAHOO_URL


class TwitterAuth(BaseAuth):
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
        request = self.oauth_request(token=None, url=TWITTER_REQUEST_TOKEN_URL)
        response = self.fetch_response(request)
        return OAuthToken.from_string(response)

    def access_token(self, token):
        request = self.oauth_request(token, TWITTER_ACCESS_TOKEN_URL)
        return OAuthToken.from_string(self.fetch_response(request))

    def user_data(self, access_token):
        request = self.oauth_request(access_token, TWITTER_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except simplejson.JSONDecodeError:
            return None

    def oauth_request(self, token, url):
        request = OAuthRequest.from_consumer_and_token(self.consumer, token=token, http_url=url)
        request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), self.consumer, token)
        return request

    def fetch_response(self, request):
        self.connection.request(request.http_method, request.to_url())
        response = self.connection.getresponse()
        return response.read()

    @property
    def connection(self):
        conn = getattr(self, '_connection', None)
        if conn is None:
            conn = httplib.HTTPSConnection(TWITTER_SERVER)
            setattr(self, '_connection', conn)
        return conn

    @property
    def consumer(self):
        cons = getattr(self, '_consumer', None)
        if cons is None:
            cons = OAuthConsumer(settings.TWITTER_CONSUMER_KEY,
                                 settings.TWITTER_CONSUMER_SECRET)
            setattr(self, '_consumer', cons)
        return cons


class FacebookAuth(BaseAuth):
    def __init__(self, request, redirect):
        super(FacebookAuth, self).__init__(request, redirect)
        self.redirect_uri = self.request.build_absolute_uri(self.redirect)
        if settings.DEBUG:
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
        params = {'access_token': access_token}
        url = FACEBOOK_CHECK_AUTH + '?' + urllib.urlencode(params)
        try:
            return simplejson.load(urllib.urlopen(url))
        except simplejson.JSONDecodeError:
            return None

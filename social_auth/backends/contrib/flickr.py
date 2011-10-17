"""
Flickr OAuth support.

This contribution adds support for Flickr OAuth service. The settings
FLICKR_APP_ID and FLICKR_API_SECRET must be defined with the values
given by Flickr application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
"""
try:
    from urlparse import parse_qs
    parse_qs # placate pyflakes
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs

from django.conf import settings
from django.utils import simplejson

from oauth2 import Token
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME

# Flickr configuration
FLICKR_SERVER = 'http://www.flickr.com/services'
FLICKR_REQUEST_TOKEN_URL = '%s/oauth/request_token' % FLICKR_SERVER
FLICKR_AUTHORIZATION_URL = '%s/oauth/authorize' % FLICKR_SERVER
FLICKR_ACCESS_TOKEN_URL = '%s/oauth/access_token' % FLICKR_SERVER
EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')


class FlickrBackend(OAuthBackend):
    """Flickr OAuth authentication backend"""
    name = 'flickr'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'), ('username', 'username'), ('expires', EXPIRES_NAME)]

    def get_user_details(self, response):
        """Return user details from Flickr account"""
        print response
        return {USERNAME: response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}

class FlickrAuth(ConsumerBasedOAuth):
    """Flickr OAuth authentication mechanism"""
    AUTHORIZATION_URL = FLICKR_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = FLICKR_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = FLICKR_ACCESS_TOKEN_URL
    SERVER_URL = FLICKR_SERVER
    AUTH_BACKEND = FlickrBackend
    SETTINGS_KEY_NAME = 'FLICKR_APP_ID'
    SETTINGS_SECRET_NAME = 'FLICKR_API_SECRET'

    def access_token(self, token):
        """Return request for access token value"""
        # Flickr is a bit different - it passes user information along with
        # the access token, so temporarily store it to vie the user_data
        # method easy access later in the flow!
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        response = self.fetch_response(request)
        token = Token.from_string(response)
        params = parse_qs(response)
        token.user_nsid = params['user_nsid'][0]
        token.fullname = params['fullname'][0]
        token.username = params['username'][0]
        return token

    def user_data(self, access_token):
        """Loads user data from service"""
        return {
            'id': access_token.user_nsid,
            'username': access_token.username,
            'fullname': access_token.fullname,
        }

# Backend definition
BACKENDS = {
    'flickr': FlickrAuth,
}

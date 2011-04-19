"""
Twitter OAuth support.

This adds support for Twitter OAuth service. An application must
be registered first on twitter and the settings TWITTER_CONSUMER_KEY
and TWITTER_CONSUMER_SECRET must be defined with they corresponding
values.

User screen name is used to generate username.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME


# Twitter configuration
TWITTER_SERVER = 'api.twitter.com'
TWITTER_REQUEST_TOKEN_URL = 'https://%s/oauth/request_token' % TWITTER_SERVER
TWITTER_ACCESS_TOKEN_URL = 'https://%s/oauth/access_token' % TWITTER_SERVER
# Note: oauth/authorize forces the user to authorize every time.
#       oauth/authenticate uses their previous selection, barring revocation.
TWITTER_AUTHORIZATION_URL = 'http://%s/oauth/authenticate' % TWITTER_SERVER
TWITTER_CHECK_AUTH = 'https://twitter.com/account/verify_credentials.json'


class TwitterBackend(OAuthBackend):
    """Twitter OAuth authentication backend"""
    name = 'twitter'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        return {USERNAME: response['screen_name'],
                'email': '',  # not supplied
                'fullname': response['name'],
                'first_name': response['name'],
                'last_name': ''}


class TwitterAuth(ConsumerBasedOAuth):
    """Twitter OAuth authentication mechanism"""
    AUTHORIZATION_URL = TWITTER_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = TWITTER_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = TWITTER_ACCESS_TOKEN_URL
    SERVER_URL = TWITTER_SERVER
    AUTH_BACKEND = TwitterBackend
    SETTINGS_KEY_NAME = 'TWITTER_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'TWITTER_CONSUMER_SECRET'

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, TWITTER_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'twitter': TwitterAuth,
}

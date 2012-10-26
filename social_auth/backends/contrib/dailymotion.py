"""
Dailymotion OAuth2 support.

This adds support for Dailymotion OAuth service. An application must
be registered first on dailymotion and the settings DAILYMOTION_CONSUMER_KEY
and DAILYMOTION_CONSUMER_SECRET must be defined with the corresponding
values.

User screen name is used to generate username.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
from django.utils import simplejson

from social_auth.utils import dsa_urlopen
from social_auth.backends import USERNAME
from social_auth.backends import BaseOAuth2
from social_auth.backends import SocialAuthBackend
from social_auth.backends.exceptions import AuthCanceled


# Dailymotion configuration
DAILYMOTION_SERVER = 'api.dailymotion.com'
DAILYMOTION_REQUEST_TOKEN_URL = 'https://%s/oauth/token' % DAILYMOTION_SERVER
DAILYMOTION_ACCESS_TOKEN_URL = 'https://%s/oauth/token' % DAILYMOTION_SERVER
# Note: oauth/authorize forces the user to authorize every time.
#       oauth/authenticate uses their previous selection, barring revocation.
DAILYMOTION_AUTHORIZATION_URL = 'https://%s/oauth/authorize' % DAILYMOTION_SERVER
DAILYMOTION_CHECK_AUTH = 'https://%s/1.1/account/verify_credentials.json' % \
                                    DAILYMOTION_SERVER


class DailymotionBackend(SocialAuthBackend):
    """Dailymotion OAuth authentication backend"""
    name = 'dailymotion'
    EXTRA_DATA = [('id', 'id')]

    def get_user_id(self, details, response):
        """Use dailymotion username as unique id"""
        return details[USERNAME]

    def get_user_details(self, response):
        return {USERNAME: response['screenname']}


class DailymotionAuth(BaseOAuth2):
    """Dailymotion OAuth2 authentication mechanism"""

    AUTHORIZATION_URL = DAILYMOTION_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = DAILYMOTION_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = DAILYMOTION_ACCESS_TOKEN_URL
    SERVER_URL = DAILYMOTION_SERVER
    AUTH_BACKEND = DailymotionBackend
    SETTINGS_KEY_NAME = 'DAILYMOTION_OAUTH2_KEY'
    SETTINGS_SECRET_NAME = 'DAILYMOTION_OAUTH2_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        request = self.oauth_request(access_token, DAILYMOTION_CHECK_AUTH)
        url = 'https://api.dailymotion.com/me/?access_token=' + access_token
        data = dsa_urlopen(url).read()
        try:
            return simplejson.loads(data)
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        else:
            return super(DailymotionAuth, self).auth_complete(*args, **kwargs)

    def oauth_request(self, token, url, extra_params=None):
        extra_params = extra_params or {}
        return extra_params


# Backend definition
BACKENDS = {
    'dailymotion': DailymotionAuth,
}

"""
Douban OAuth support.

This adds support for Douban OAuth service. An application must
be registered first on douban.com and the settings DOUBAN_CONSUMER_KEY
and DOUBAN_CONSUMER_SECRET must be defined with they corresponding
values.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME
from social_auth.backends.exceptions import AuthCanceled


DOUBAN_SERVER = 'www.douban.com'
DOUBAN_REQUEST_TOKEN_URL = 'http://%s/service/auth/request_token' % \
                                DOUBAN_SERVER
DOUBAN_ACCESS_TOKEN_URL = 'http://%s/service/auth/access_token' % \
                                DOUBAN_SERVER

DOUBAN_AUTHORIZATION_URL = 'http://%s/service/auth/authorize' % \
                                DOUBAN_SERVER


class DoubanBackend(OAuthBackend):
    """Douban OAuth authentication backend"""
    name = 'douban'
    EXTRA_DATA = [('id', 'id')]

    def get_user_id(self, details, response):
        return response['db:uid']['$t']

    def get_user_details(self, response):
        """Return user details from Douban"""
        return {USERNAME: response["db:uid"]["$t"],
                'email': ''}


class DoubanAuth(ConsumerBasedOAuth):
    """Douban OAuth authentication mechanism"""
    AUTHORIZATION_URL = DOUBAN_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = DOUBAN_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = DOUBAN_ACCESS_TOKEN_URL
    SERVER_URL = DOUBAN_SERVER
    AUTH_BACKEND = DoubanBackend
    SETTINGS_KEY_NAME = 'DOUBAN_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'DOUBAN_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        url = 'http://api.douban.com/people/%40me?&alt=json'
        request = self.oauth_request(access_token, url)
        json = self.fetch_response(request)

        try:
            return simplejson.loads(json)
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        else:
            return super(DoubanAuth, self).auth_complete(*args, **kwargs)


# Backend definition
BACKENDS = {
    'douban': DoubanAuth,
}

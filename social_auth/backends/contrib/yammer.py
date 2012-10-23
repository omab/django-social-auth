"""
Yammer OAuth2 support
"""
from urllib import urlencode
import logging

from django.utils import simplejson

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import dsa_urlopen, setting

YAMMER_OAUTH_URL = 'https://www.yammer.com/oauth/'
YAMMER_AUTH_URL = 'https://www.yammer.com/dialog/oauth'
YAMMER_API_URL = 'https://www.yammer.com/api/v1/'

class YammerBackend(OAuthBackend):
    name = 'yammer'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        logging.error(response)

        first_name = last_name = email = None
        full_name = response.get('full_name', '')

        try:
            parts = full_name.split(' ')
            first_name = parts[0]
            last_name = parts[1]
        except:
            pass

        try:
            email = response['contact']['email_addresses'][0]['address']
        except:
            pass

        return {USERNAME: response.get('name', ''),
                'email': email,
                'fullname': full_name,
                'first_name': first_name,
                'last_name': last_name}

class YammerOAuth2(BaseOAuth2):
    AUTH_BACKEND = YammerBackend
    AUTHORIZATION_URL = YAMMER_AUTH_URL
    ACCESS_TOKEN_URL = '%s%s' % (YAMMER_OAUTH_URL, 'access_token')
    REQUEST_TOKEN_URL = '%s%s' % (YAMMER_OAUTH_URL, 'request_token')

    SETTINGS_KEY_NAME = 'YAMMER_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'YAMMER_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Load user data from yammer"""
        # /users/[:id].json
        params = {
            'client_id': setting(self.SETTINGS_KEY_NAME, ''),
            'client_secret': setting(self.SETTINGS_SECRET_NAME, ''),
            'code': access_token
        }
        url = '%s?%s' % (ACCESS_TOKEN_URL, urlencode(params))
        try:
            return simplejson.load(dsa_urlopen(url))
        except Exception, e:
            logging.exception(e)
        return None

BACKENDS = {
    'yammer': YammerOAuth2,
}


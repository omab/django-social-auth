"""
Yammer OAuth2 support
"""
from urllib import urlencode
from urlparse import parse_qs
import logging

from django.utils import simplejson
from django.utils.datastructures import MergeDict

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.backends.exceptions import AuthCanceled
from social_auth.utils import dsa_urlopen, setting

YAMMER_OAUTH_URL = 'https://www.yammer.com/oauth2/'
YAMMER_AUTH_URL = 'https://www.yammer.com/dialog/oauth'
YAMMER_API_URL = 'https://www.yammer.com/api/v1/'

class YammerBackend(OAuthBackend):
    name = 'yammer'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires')),
        ('picture_url', 'mugshot_url')
    ]

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        logging.error(response)

        username = response['user']['name']
        first_name = response['user']['first_name']
        last_name = response['user']['last_name']
        full_name = response['user']['full_name']
        email = response['user']['contact']['email_addresses'][0]['address']
        mugshot_url = response['user']['mugshot_url']

        user_data = {
            USERNAME: username,
            'email': email,
            'fullname': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'picture_url': mugshot_url
        }

        return user_data

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
        url = '%s?%s' % (self.ACCESS_TOKEN_URL, urlencode(params))
        try:
            return simplejson.load(dsa_urlopen(url))
        except Exception, e:
            logging.exception(e)
        return None
    
    def auth_complete(self, *args, **kwargs):
        """Yammer API is a little strange"""
        if 'error' in self.data:
            logging.error("%s: %s:\n%s" % (
                self.data('error'), self.data('error_reason'),
                self.data('error_description')
            ))
            raise AuthCanceled(self)

        # now we need to clean up the data params
        data = dict(self.data.copy())
        redirect_state = data.get('redirect_state')
        try:
            parts = redirect_state.split('?')
            data['redirect_state'] = parts[0]
            extra = parse_qs(parts[1])
            data['code'] = extra['code'][0]
            self.data = MergeDict(data)
        except Exception as e:
            logging.exception(e)

        return super(YammerOAuth2, self).auth_complete(*args, **kwargs)

BACKENDS = {
    'yammer': YammerOAuth2,
}


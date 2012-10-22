"""
Yammer OAuth2 support
"""
from urllib import urlencode
from urllib2 import Request

from django.utils import simplejson

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import dsa_urlopen

YAMMER_OAUTH_URL = 'https://www.yammer.com/oauth/'
YAMMER_API_URL = 'https://www.yammer.com/api/v1/'

class YammerBackend(OAuthBackend):
    name = 'yammer'
    EXTRA_DATA = [
            
    ]

    def get_user_details(self, response):
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
                'email': None,
                'fullname': full_name,
                'first_name': first_name,
                'last_name': last_name}

class YammerOAuth2(BaseOAuth2):
    AUTH_BACKEND = YammerBackend
    AUTHORIZATION_URL = '%s%s' % (YAMMER_OAUTH_URL, 'authorize')
    ACCESS_TOKEN_URL = '%s%s' % (YAMMER_OAUTH_URL, 'access_token')
    REQUEST_TOKEN_URL = '%s%s' % (YAMMER_OAUTH_URL, 'request_token')

    SETTINGS_KEY_NAME = 'YAMMER_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'YAMMER_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        return mixcloud_profile(access_token)

def mixcloud_profile(access_token):

    data = {'access_token': access_token, 'alt': 'json'}
    request = Request(MIXCLOUD_PROFILE_URL + '?' + urlencode(data))

    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except (ValueError, KeyError, IOError):
        return None

BACKENDS = {
    'yammer': YammerOAuth2,
}


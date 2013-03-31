from urllib2 import Request, urlopen, HTTPError
from urllib import urlencode

from django.utils import simplejson

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME


# Jawbone configuration
JAWBONE_SERVER = 'https://jawbone.com/'
JAWBONE_AUTHORIZATION_URL = '%s/auth/oauth2/auth' % JAWBONE_SERVER
JAWBONE_ACCESS_TOKEN_URL = '%s/auth/oauth2/token' % JAWBONE_SERVER
JAWBONE_CHECK_AUTH = '%s/nudge/api/users/@me' % JAWBONE_SERVER


class JawboneBackend(OAuthBackend):
    name = 'jawbone'

    def get_user_id(self, details, response):
        return response['data']['xid']

    def get_user_details(self, response):
        """Return user details from Jawbone account. Jawbone does not collect emails"""
        firstName = response['data'].get('first', '')
        lastName = response['data'].get('last', '')
        dob = response['data'].get('dob', '')
        gender = response['data'].get('gender', '')
        height = response['data'].get('height', '')
        weight = response['data'].get('weight', '')

        return {USERNAME: firstName + ' ' + lastName,
                'first_name': firstName,
                'last_name': lastName,
                'dob': dob,
                'gender': gender,
                'height': height,
                'weight': weight}


class JawboneAuth(BaseOAuth2):
    """Jawbone OAuth mechanism"""
    AUTHORIZATION_URL = JAWBONE_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = JAWBONE_ACCESS_TOKEN_URL
    SERVER_URL = JAWBONE_SERVER
    AUTH_BACKEND = JawboneBackend
    SETTINGS_KEY_NAME = 'JAWBONE_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'JAWBONE_CONSUMER_SECRET'
    SCOPE_SEPARATOR = ' '
    # Look at http://developer.github.com/v3/oauth/
    SCOPE_VAR_NAME = 'JAWBONE_EXTENDED_PERMISSIONS'

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = JAWBONE_CHECK_AUTH
        headers = {'Authorization': 'Bearer ' + access_token}
        request = Request(url, headers=headers)
        try:
            return simplejson.load(urlopen(request))
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'jawbone': JawboneAuth,
    }

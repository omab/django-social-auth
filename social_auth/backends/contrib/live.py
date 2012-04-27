"""
MSN Live Connect oAuth 2.0

Settings:
LIVE_CLIENT_ID
LIVE_CLIENT_SECRET
LIVE_EXTENDED_PERMISSIONS (default: wl.basic, wl.emails)

References:
* oAuth  http://msdn.microsoft.com/en-us/library/live/hh243649.aspx
* Scopes http://msdn.microsoft.com/en-us/library/live/hh243646.aspx
* REST   http://msdn.microsoft.com/en-us/library/live/hh243648.aspx
"""
from urllib import urlencode, urlopen

from django.utils import simplejson

from social_auth.utils import setting
from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME


# Live Connect configuration
LIVE_AUTHORIZATION_URL    = 'https://login.live.com/oauth20_authorize.srf'
LIVE_ACCESS_TOKEN_URL     = 'https://login.live.com/oauth20_token.srf'
LIVE_USER_DATA_URL        = 'https://apis.live.net/v5.0/me'
LIVE_SERVER               = 'live.com'
LIVE_EXTENDED_PERMISSIONS = ['wl.basic', 'wl.emails']


class LiveBackend(OAuthBackend):
    name = 'live'

    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires')),
        ('email', 'email'),
        ('first_name', 'first_name'),
        ('last_name', 'last_name'),
    ]

    def get_user_id(self, details, response):
        return response['id']

    def get_user_details(self, response):
        """Return user details from Github account"""
        try:
            email = response['emails']['account']
        except KeyError:
            email = ''

        return {USERNAME:     response.get('name'),
                'email':      email,
                'first_name': response.get('first_name'),
                'last_name':  response.get('last_name')}


class LiveAuth(BaseOAuth2):
    AUTHORIZATION_URL    = LIVE_AUTHORIZATION_URL
    ACCESS_TOKEN_URL     = LIVE_ACCESS_TOKEN_URL
    SERVER_URL           = LIVE_SERVER
    AUTH_BACKEND         = LiveBackend
    SETTINGS_KEY_NAME    = 'LIVE_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'LIVE_CLIENT_SECRET'
    SCOPE_SEPARATOR      = ','

    def get_scope(self):
        """Return list with needed access scope"""
        return setting('LIVE_EXTENDED_PERMISSIONS', LIVE_EXTENDED_PERMISSIONS)

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = LIVE_USER_DATA_URL + '?' + urlencode({
            'access_token': access_token
        })
        try:
            return simplejson.load(urlopen(url))
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'live': LiveAuth,
}

import urllib

from django.utils import simplejson

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME


INSTAGRAM_SERVER = 'instagram.com'
INSTAGRAM_AUTHORIZATION_URL = 'https://instagram.com/oauth/authorize'
INSTAGRAM_ACCESS_TOKEN_URL = 'https://instagram.com/oauth/access_token'
INSTAGRAM_CHECK_AUTH = 'https://api.instagram.com/v1/users/self'


class InstagramBackend(OAuthBackend):
    name = 'instagram'

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        """Return user details from Instagram account"""
        username = response['user']['username']
        fullname = response['user'].get('fullname', '')
        email = response['user'].get('email', '')
        return {
            USERNAME: username,
            'first_name': fullname,
            'email': email
        }


class InstagramAuth(BaseOAuth2):
    """Instagram OAuth mechanism"""
    AUTHORIZATION_URL = INSTAGRAM_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = INSTAGRAM_ACCESS_TOKEN_URL
    SERVER_URL = INSTAGRAM_SERVER
    AUTH_BACKEND = InstagramBackend
    SETTINGS_KEY_NAME = 'INSTAGRAM_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'INSTAGRAM_CLIENT_SECRET'

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'access_token': access_token}
        url = INSTAGRAM_CHECK_AUTH + '?' + urllib.urlencode(params)
        try:
            return simplejson.load(urllib.urlopen(url))
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'instagram': InstagramAuth,
}

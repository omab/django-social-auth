"""
GitHub OAuth support.

This contribution adds support for GitHub OAuth service. The settings
GITHUB_APP_ID and GITHUB_API_SECRET must be defined with the values
given by GitHub application registration process.

Extended permissions are supported by defining GITHUB_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from urllib import urlencode

from django.utils import simplejson

from social_auth.utils import setting, dsa_urlopen
from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME


# GitHub configuration
GITHUB_AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_DATA_URL = 'https://api.github.com/user'
GITHUB_SERVER = 'github.com'


class GithubBackend(OAuthBackend):
    """Github OAuth authentication backend"""
    name = 'github'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {USERNAME: response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}


class GithubAuth(BaseOAuth2):
    """Github OAuth2 mechanism"""
    AUTHORIZATION_URL = GITHUB_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = GITHUB_ACCESS_TOKEN_URL
    SERVER_URL = GITHUB_SERVER
    AUTH_BACKEND = GithubBackend
    SETTINGS_KEY_NAME = 'GITHUB_APP_ID'
    SETTINGS_SECRET_NAME = 'GITHUB_API_SECRET'
    SCOPE_SEPARATOR = ','
    # Look at http://developer.github.com/v3/oauth/
    SCOPE_VAR_NAME = 'GITHUB_EXTENDED_PERMISSIONS'

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = GITHUB_USER_DATA_URL + '?' + urlencode({
            'access_token': access_token
        })
        try:
            return simplejson.load(dsa_urlopen(url))
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'github': GithubAuth,
}

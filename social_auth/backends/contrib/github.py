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
import cgi
from urllib import urlencode, urlopen

from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.utils import setting
from social_auth.backends import BaseOAuth, OAuthBackend, USERNAME
from social_auth.backends.exceptions import AuthFailed


# GitHub configuration
GITHUB_AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize?'
GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token?'
GITHUB_USER_DATA_URL = 'https://api.github.com/user?'


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


class GithubAuth(BaseOAuth):
    """Github OAuth mechanism"""
    AUTH_BACKEND = GithubBackend

    def auth_url(self):
        """Returns redirect url"""
        args = {
            'client_id': setting('GITHUB_APP_ID'),
            'redirect_uri': self.redirect_uri
        }
        if setting('GITHUB_EXTENDED_PERMISSIONS'):
            args['scope'] = ','.join(setting('GITHUB_EXTENDED_PERMISSIONS'))
        args.update(self.auth_extra_arguments())
        return GITHUB_AUTHORIZATION_URL + urlencode(args)

    def auth_complete(self, *args, **kwargs):
        """Returns user, might be logged in"""
        if 'code' not in self.data:
            error = self.data.get('error') or 'unknown error'
            raise AuthFailed(self, error)

        url = GITHUB_ACCESS_TOKEN_URL + urlencode({
              'client_id': setting('GITHUB_APP_ID'),
              'redirect_uri': self.redirect_uri,
              'client_secret': setting('GITHUB_API_SECRET'),
              'code': self.data['code']
        })
        response = cgi.parse_qs(urlopen(url).read())
        if response.get('error'):
            error = self.data.get('error') or 'unknown error'
            raise AuthFailed(self, error)

        access_token = response['access_token'][0]
        data = self.user_data(access_token)
        if data is not None:
            if 'error' in data:
                error = self.data.get('error') or 'unknown error'
                raise AuthFailed(self, error)
            data['access_token'] = access_token

        kwargs.update({
            'auth': self,
            'response': data,
            self.AUTH_BACKEND.name: True
        })
        return authenticate(*args, **kwargs)

    def user_data(self, access_token):
        """Loads user data from service"""
        url = GITHUB_USER_DATA_URL + urlencode({
            'access_token': access_token
        })
        try:
            return simplejson.load(urlopen(url))
        except ValueError:
            return None

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return setting('GITHUB_APP_ID') and setting('GITHUB_API_SECRET')


# Backend definition
BACKENDS = {
    'github': GithubAuth,
}

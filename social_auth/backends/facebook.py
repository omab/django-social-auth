"""
Facebook OAuth support.

This contribution adds support for Facebook OAuth service. The settings
FACEBOOK_APP_ID and FACEBOOK_API_SECRET must be defined with the values
given by Facebook application registration process.

Extended permissions are supported by defining FACEBOOK_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import cgi
from urllib import urlencode
from urllib2 import urlopen, HTTPError

from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import sanitize_log_data, setting, log
from social_auth.backends.exceptions import AuthException, AuthCanceled, \
                                            AuthFailed, AuthTokenError


# Facebook configuration
FACEBOOK_ME = 'https://graph.facebook.com/me?'
ACCESS_TOKEN = 'https://graph.facebook.com/oauth/access_token?'


class FacebookBackend(OAuthBackend):
    """Facebook OAuth2 authentication backend"""
    name = 'facebook'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {USERNAME: response.get('username'),
                'email': response.get('email', ''),
                'fullname': response.get('name', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}


class FacebookAuth(BaseOAuth2):
    """Facebook OAuth2 support"""
    AUTH_BACKEND = FacebookBackend
    RESPONSE_TYPE = None
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = 'https://www.facebook.com/dialog/oauth'
    SETTINGS_KEY_NAME = 'FACEBOOK_APP_ID'
    SETTINGS_SECRET_NAME = 'FACEBOOK_API_SECRET'

    def get_scope(self):
        return setting('FACEBOOK_EXTENDED_PERMISSIONS', [])

    def user_data(self, access_token):
        """Loads user data from service"""
        data = None
        url = FACEBOOK_ME + urlencode({'access_token': access_token})

        try:
            data = simplejson.load(urlopen(url))
        except ValueError:
            extra = {'access_token': sanitize_log_data(access_token)}
            log('error', 'Could not load user data from Facebook.',
                exc_info=True, extra=extra)
        except HTTPError:
            extra = {'access_token': sanitize_log_data(access_token)}
            log('error', 'Error validating access token.',
                exc_info=True, extra=extra)
            raise AuthTokenError(self)
        else:
            log('debug', 'Found user data for token %s',
                sanitize_log_data(access_token), extra={'data': data})
        return data

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'code' not in self.data:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)

        url = ACCESS_TOKEN + urlencode({
            'client_id': setting('FACEBOOK_APP_ID'),
            'redirect_uri': self.redirect_uri,
            'client_secret': setting('FACEBOOK_API_SECRET'),
            'code': self.data['code']
        })
        try:
            response = cgi.parse_qs(urlopen(url).read())
        except HTTPError:
            raise AuthFailed(self, 'There was an error authenticating the app')

        access_token = response['access_token'][0]
        data = self.user_data(access_token)

        if data is not None:
            data['access_token'] = access_token
            # expires will not be part of response if offline access
            # premission was requested
            if 'expires' in response:
                data['expires'] = response['expires'][0]

        kwargs.update({'auth': self,
                       'response': data,
                       self.AUTH_BACKEND.name: True})
        return authenticate(*args, **kwargs)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return setting('FACEBOOK_APP_ID') and setting('FACEBOOK_API_SECRET')


# Backend definition
BACKENDS = {
    'facebook': FacebookAuth,
}

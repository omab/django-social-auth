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
import base64
import hmac
import hashlib
import time
from urllib import urlencode
from urllib2 import HTTPError

from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import sanitize_log_data, backend_setting, setting, \
                              log, dsa_urlopen
from social_auth.backends.exceptions import AuthException, AuthCanceled, \
                                            AuthFailed, AuthTokenError, \
                                            AuthUnknownError


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
        return {USERNAME: response.get('username', response.get('name')),
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
    SCOPE_VAR_NAME = 'FACEBOOK_EXTENDED_PERMISSIONS'
    EXTRA_PARAMS_VAR_NAME = 'FACEBOOK_PROFILE_EXTRA_PARAMS'

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        data = None
        params = backend_setting(self, self.EXTRA_PARAMS_VAR_NAME, {})
        params['access_token'] = access_token
        url = FACEBOOK_ME + urlencode(params)

        try:
            data = simplejson.load(dsa_urlopen(url))
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
        access_token = None
        expires = None

        if 'code' in self.data:
            state = self.validate_state()
            url = ACCESS_TOKEN + urlencode({
                'client_id': backend_setting(self, self.SETTINGS_KEY_NAME),
                'redirect_uri': self.get_redirect_uri(state),
                'client_secret': backend_setting(self,
                                                 self.SETTINGS_SECRET_NAME),
                'code': self.data['code']
            })
            try:
                response = cgi.parse_qs(dsa_urlopen(url).read())
            except HTTPError:
                raise AuthFailed(self, 'There was an error authenticating '
                                       'the app')

            access_token = response['access_token'][0]
            if 'expires' in response:
                expires = response['expires'][0]

        if 'signed_request' in self.data:
            response = load_signed_request(self.data.get('signed_request'),
                                           backend_setting(
                                               self,
                                               self.SETTINGS_SECRET_NAME))

            if response is not None:
                access_token = response.get('access_token') or \
                               response.get('oauth_token') or \
                               self.data.get('access_token')

                if 'expires' in response:
                    expires = response['expires']

        if access_token:
            data = self.user_data(access_token)

            if not isinstance(data, dict):
                # From time to time Facebook responds back a JSON with just
                # False as value, the reason is still unknown, but since the
                # data is needed (it contains the user ID used to identify the
                # account on further logins), this app cannot allow it to
                # continue with the auth process.
                raise AuthUnknownError(self, 'An error ocurred while '
                                             'retrieving users Facebook '
                                             'data')

            data['access_token'] = access_token
            # expires will not be part of response if offline access
            # premission was requested
            if expires:
                data['expires'] = expires

            kwargs.update({'auth': self,
                           'response': data,
                           self.AUTH_BACKEND.name: True})

            return authenticate(*args, **kwargs)
        else:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return backend_setting(cls, cls.SETTINGS_KEY_NAME) and \
               backend_setting(cls, cls.SETTINGS_SECRET_NAME)


def base64_url_decode(data):
    data = data.encode(u'ascii')
    data += '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data)


def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip('=')


def load_signed_request(signed_request, api_secret=None):
    try:
        sig, payload = signed_request.split(u'.', 1)
        sig = base64_url_decode(sig)
        data = simplejson.loads(base64_url_decode(payload))

        expected_sig = hmac.new(api_secret or setting('FACEBOOK_API_SECRET'),
                                msg=payload,
                                digestmod=hashlib.sha256).digest()

        # allow the signed_request to function for upto 1 day
        if sig == expected_sig and \
                data[u'issued_at'] > (time.time() - 86400):
            return data
    except ValueError:
        pass  # ignore if can't split on dot


# Backend definition
BACKENDS = {
    'facebook': FacebookAuth,
}

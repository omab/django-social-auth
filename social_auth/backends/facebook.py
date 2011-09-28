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
import logging
logger = logging.getLogger(__name__)

import cgi
from urllib import urlencode
from urllib2 import urlopen

from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import sanitize_log_data


# Facebook configuration
EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')


class FacebookBackend(OAuthBackend):
    """Facebook OAuth2 authentication backend"""
    name = 'facebook'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'), ('expires', EXPIRES_NAME)]

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {USERNAME: response.get('username') or response['name'],
                'email': response.get('email', ''),
                'fullname': response['name'],
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
        return getattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS', [])

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'access_token': access_token,}
        url = 'https://graph.facebook.com/me?' + urlencode(params)
        try:
            data = simplejson.load(urlopen(url))
            logger.debug('Found user data for token %s',
                         sanitize_log_data(access_token),
                         extra=dict(data=data))
            return data

        except ValueError:
            params.update({'access_token': sanitize_log_data(access_token)})
            logger.error('Could not load user data from Facebook.',
                         exc_info=True, extra=dict(data=params))
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'code' in self.data:
            url = 'https://graph.facebook.com/oauth/access_token?' + \
                  urlencode({'client_id': settings.FACEBOOK_APP_ID,
                             'redirect_uri': self.redirect_uri,
                             'client_secret': settings.FACEBOOK_API_SECRET,
                             'code': self.data['code']})
            response = cgi.parse_qs(urlopen(url).read())
            access_token = response['access_token'][0]
            data = self.user_data(access_token)
            if data is not None:
                if 'error' in data:
                    error = self.data.get('error') or 'unknown error'
                    raise ValueError('Authentication error: %s' % error)
                data['access_token'] = access_token
                # expires will not be part of response if offline access
                # premission was requested
                if 'expires' in response:
                    data['expires'] = response['expires'][0]
            kwargs.update({'response': data, self.AUTH_BACKEND.name: True})
            return authenticate(*args, **kwargs)
        else:
            error = self.data.get('error') or 'unknown error'
            raise ValueError('Authentication error: %s' % error)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in ('FACEBOOK_APP_ID',
                                                        'FACEBOOK_API_SECRET'))


# Backend definition
BACKENDS = {
    'facebook': FacebookAuth,
}

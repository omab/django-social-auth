"""
Fitbit OAuth support.

This contribution adds support for Fitbit OAuth service. The settings
FITBIT_CONSUMER_KEY and FITBIT_CONSUMER_SECRET must be defined with the values
given by Fitbit application registration process.

Extended permissions are supported by defining FITBIT_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import logging
logger = logging.getLogger('buttekicker')

import cgi
import urllib

from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth, OAuthBackend, USERNAME


# Fitbit configuration
FITBIT_SERVER = 'api.fitbit.com'
FITBIT_REQUEST_TOKEN_URL = 'https://%s/oauth/request_token' % FITBIT_SERVER
FITBIT_AUTHORIZATION_URL = 'https://%s/oauth/authorize' % FITBIT_SERVER
FITBIT_ACCESS_TOKEN_URL = 'https://%s/oauth/access_token' % FITBIT_SERVER
FITBIT_API_URL = 'https://api.%s' % FITBIT_SERVER
EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')


class FitbitBackend(OAuthBackend):
    """Fitbit OAuth authentication backend"""
    name = 'fitbit'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'), ('expires', EXPIRES_NAME)]

    def get_user_details(self, response):
        """Return user details from Fitbit account"""
        return {USERNAME: response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}

class FitbitAuth(BaseOAuth):
    """Fitbit OAuth mechanism"""
    AUTH_BACKEND = FitbitBackend

    def auth_url(self):
        """Returns redirect url"""
        args = {'client_id': settings.FITBIT_CONSUMER_KEY,
                'redirect_uri': self.redirect_uri}
        if hasattr(settings, 'FITBIT_EXTENDED_PERMISSIONS'):
            args['scope'] = ','.join(settings.FITBIT_EXTENDED_PERMISSIONS)
        args.update(self.auth_extra_arguments())
        return FITBIT_AUTHORIZATION_URL + '?' + urllib.urlencode(args)

    def auth_complete(self, *args, **kwargs):
        """Returns user, might be logged in"""
        if 'code' in self.data:
            url = FITBIT_ACCESS_TOKEN_URL + '?' + \
                  urllib.urlencode({'client_id': settings.FITBIT_CONSUMER_KEY,
                                'redirect_uri': self.redirect_uri,
                                'client_secret': settings.FITBIT_CONSUMER_SECRET,
                                'code': self.data['code']})
            response = cgi.parse_qs(urllib.urlopen(url).read())
            if response.get('error'):
                error = self.data.get('error') or 'unknown error'
                raise ValueError('Authentication error: %s' % error)
            access_token = response['access_token'][0]
            data = self.user_data(access_token)
            if data is not None:
                if 'error' in data:
                    error = self.data.get('error') or 'unknown error'
                    raise ValueError('Authentication error: %s' % error)
                data['access_token'] = access_token
            kwargs.update({'response': data, FitbitBackend.name: True})
            return authenticate(*args, **kwargs)
        else:
            error = self.data.get('error') or 'unknown error'
            raise ValueError('Authentication error: %s' % error)

    def user_data(self, access_token):
        """Loads user data from service"""
        params = {'access_token': access_token}
        url = FITBIT_API_URL + '/user?' + urllib.urlencode(params)
        try:
            return simplejson.load(urllib.urlopen(url))
        except ValueError:
            return None

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in
                        ('FITBIT_CONSUMER_KEY',
                         'FITBIT_CONSUMER_SECRET'))


# Backend definition
BACKENDS = {
    'fitbit': FitbitAuth,
}

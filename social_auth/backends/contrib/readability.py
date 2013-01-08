"""
Readability OAuth support.

This contribution adds support for Readability OAuth service. The settings
READABILITY_CONSUMER_KEY and READABILITY_CONSUMER_SECRET must be defined with
the values given by Readability in the Connections page of your account settings.

"""
from urllib import urlencode

from django.utils import simplejson

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME
from social_auth.exceptions import AuthCanceled
from social_auth.utils import setting

# Readability configuration
READABILITY_SERVER = 'www.readability.com'
READABILITY_AUTHORIZATION_URL = 'https://%s/api/rest/v1/oauth/authorize/' % READABILITY_SERVER
READABILITY_ACCESS_TOKEN_URL = 'https://%s/api/rest/v1/oauth/access_token/' % READABILITY_SERVER
READABILITY_REQUEST_TOKEN_URL = 'https://%s/api/rest/v1/oauth/request_token/' % READABILITY_SERVER
READABILITY_USER_DATA_URL = 'https://%s/api/rest/v1/users/_current' % READABILITY_SERVER

class ReadabilityBackend(OAuthBackend):
    """Readability OAuth authentication backend"""
    name = 'readability'

    EXTRA_DATA = [('date_joined', 'date_joined'),
                  ('kindle_email_address', 'kindle_email_address'),
                  ('avatar_url', 'avatar_url')]

    def get_user_details(self, response):
        username = response['username']
        first_name, last_name = response['first_name'], response['last_name']
        date_joined = response['date_joined']

        return {USERNAME: username,
                'fullname': first_name + ' ' + last_name,
                'first_name': first_name,
                'last_name': last_name}

    def get_user_id(self, response):
        """Returns a unique username to use"""
        return response['username']

class ReadabilityAuth(ConsumerBasedOAuth):
    """Readability OAuth authentication mechanism"""
    AUTHORIZATION_URL = READABILITY_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = READABILITY_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = READABILITY_ACCESS_TOKEN_URL
    SERVER_URL = READABILITY_SERVER
    AUTH_BACKEND = ReadabilityBackend
    SETTINGS_KEY_NAME = 'READABILITY_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'READABILITY_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        url = READABILITY_USER_DATA_URL
        request = self.oauth_request(access_token, url)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'error' in self.data:
            raise AuthCanceled(self)
        else:
            return super(ReadabilityAuth, self).auth_complete(*args, **kwargs)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""

        return setting('READABILITY_CONSUMER_KEY') and setting('READABILITY_CONSUMER_SECRET')

BACKENDS = {
    'readability': ReadabilityAuth,
}
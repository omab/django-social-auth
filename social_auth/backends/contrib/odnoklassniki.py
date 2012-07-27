"""
Odnoklassniki.ru OAuth2 support

Take a look to:
http://dev.odnoklassniki.ru/wiki/display/ok/The+OAuth+2.0+Protocol

You need to register OAuth application here:
http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=13992188

Then setup your application according manual and use information from
registration mail to set settings values.
"""
from django.conf import settings
from django.utils import simplejson

from urllib import urlencode, unquote
from urllib2 import Request
from hashlib import md5

from social_auth.backends import OAuthBackend, BaseOAuth2, USERNAME
from social_auth.utils import setting, log, dsa_urlopen

ODNOKLASSNIKI_API_URL = 'http://api.odnoklassniki.ru/fb.do'
ODNOKLASSNIKI_OAUTH2_SCOPE = ['']  # Enough for authentication

EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')


class OdnoklassnikiBackend(OAuthBackend):
    """Odnoklassniki authentication backend"""
    name = 'odnoklassniki'
    EXTRA_DATA = [('refresh_token', 'refresh_token'),
                  ('expires_in', EXPIRES_NAME)]

    def get_user_id(self, details, response):
        """Return user unique id provided by Odnoklassniki"""
        return response['uid']

    def get_user_details(self, response):
        """Return user details from Odnoklassniki request"""
        return {
            USERNAME: response['uid'],
            'email': '',
            'fullname': unquote(response['name']),
            'first_name': unquote(response['first_name']),
            'last_name': unquote(response['last_name'])
        }


class OdnoklassnikiOAuth2(BaseOAuth2):
    """Odnoklassniki OAuth2 support"""
    AUTH_BACKEND = OdnoklassnikiBackend
    AUTHORIZATION_URL = 'http://www.odnoklassniki.ru/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://api.odnoklassniki.ru/oauth/token.do'
    SETTINGS_KEY_NAME = 'ODNOKLASSNIKI_OAUTH2_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET'
    FORCE_STATE_CHECK = False

    def get_scope(self):
        return setting('ODNOKLASSNIKI_OAUTH2_EXTRA_SCOPE', [])

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Odnoklassniki REST API"""
        data = {'access_token': access_token, 'method': 'users.getCurrentUser'}
        return odnoklassniki_api(data)


def odnoklassniki_sig(data):
    """Calculates signature of request data access_token value must be
    included"""
    suffix = md5(data['access_token'] +
                 settings.ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET).hexdigest()
    check_list = sorted(list(item + '=' + data[item]
                                for item in data
                                    if item != 'access_token'))
    return md5(''.join(check_list) + suffix).hexdigest()


def odnoklassniki_api(data):
    """ Calls Odnoklassniki REST API method
        http://dev.odnoklassniki.ru/wiki/display/ok/Odnoklassniki+Rest+API
    """
    data.update({
        'application_key': settings.ODNOKLASSNIKI_OAUTH2_APP_KEY,
        'format': 'JSON'
    })
    data['sig'] = odnoklassniki_sig(data)

    params = urlencode(data)
    request = Request(ODNOKLASSNIKI_API_URL + '?' + params)
    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        log('error', 'Could not load data from Odnoklassniki.',
            exc_info=True, extra=dict(data=params))
        return None


# Backend definition
BACKENDS = {
    'odnoklassniki': OdnoklassnikiOAuth2
}

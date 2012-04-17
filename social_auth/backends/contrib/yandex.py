"""
Yandex OAuth support.

"""
from urllib import urlencode, urlopen
from urlparse import urlparse

from django.utils import simplejson

from social_auth.utils import setting
from social_auth.backends import BaseOAuth2, OAuthBackend, OpenIdAuth, \
                                 OpenIDBackend, USERNAME


# Vkontakte configuration
YANDEX_AUTHORIZATION_URL = 'https://oauth.yandex.ru/authorize'
YANDEX_ACCESS_TOKEN_URL = 'https://oauth.yandex.ru/token'
YANDEX_USER_DATA_URL = 'https://api.vk.com/method/users.get'
YANDEX_USER_ID_URL = 'https://api-yaru.yandex.ru/me/'
YANDEX_SERVER = 'oauth.yandex.ru'
YANDEX_OPENID_URL = 'http://openid.yandex.ru'


def get_username_from_url(links):
    try:
        host = urlparse(links.get('www')).hostname
        return host.split('.')[0]
    except (IndexError, AttributeError):
        return None


class YandexBackend(OpenIDBackend):
    """Yandex OpenID authentication backend"""
    name = 'yandex'

    def get_user_id(self, details, response):
        #validate_whitelists(self, details['email'])
        return details['email']

class YandexAuth(OpenIdAuth):
    """Yandex OpenID authentication"""
    AUTH_BACKEND = YandexBackend

    def openid_url(self):
        """Return Google OpenID service url"""
        return YANDEX_OPENID_URL

class YaruBackend(OAuthBackend):
    """Yandex OAuth authentication backend"""
    name = 'yaru'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_details(self, response):
        """Return user details from Vkontakte account"""
        return { USERNAME: get_username_from_url(response.get('links')),
                 'email':  response.get('email'),
                 'first_name': response.get('name'),
               } 


class YaruAuth(BaseOAuth2):
    """Yandex OAuth mechanism"""
    AUTHORIZATION_URL = YANDEX_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = YANDEX_ACCESS_TOKEN_URL
    SERVER_URL = YANDEX_SERVER
    AUTH_BACKEND = YaruBackend 
    SETTINGS_KEY_NAME = 'YANDEX_APP_ID'
    SETTINGS_SECRET_NAME = 'YANDEX_API_SECRET'

    def user_data(self, access_token, response, *args, **kwargs):
        """Loads user data from service"""
        params = {'oauth_token': access_token,
                  'format': 'json',
                 }
        headers = {'Content-Type': 'application/x-yaru+json; type=person',
                    'Accept': 'application/x-yaru+json'}

        url = YANDEX_USER_ID_URL + '?' + urlencode(params)
        try:
            return simplejson.load(urlopen(url))
        except (ValueError, IndexError):
            return None



# Backend definition
BACKENDS = {
    'yandex': YandexAuth,
    'yaru': YaruAuth,
}

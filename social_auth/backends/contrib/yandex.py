"""
Yandex OpenID support.

This contribution adds support for Yandex.ru OpenID service in the form
openid.yandex.ru/user. Username is retrieved from the identity url.

If username is not specified, OpenID 2.0 url used for authentication.
"""
import urlparse

from social_auth.backends import OpenIDBackend, OpenIdAuth, USERNAME


# Yandex conf
YANDEX_URL = 'http://openid.yandex.ru/%s'
YANDEX_USER_FIELD = 'openid_ya_user'
YANDEX_OID_2_URL = 'http://yandex.ru'


class YandexBackend(OpenIDBackend):
    """Yandex OpenID authentication backend"""
    name = 'yandex'

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super(YandexBackend, self).get_user_details(response)
        values[USERNAME] = values.get(USERNAME) or \
                           urlparse.urlsplit(response.identity_url)\
                                   .path.strip('/')
                                   
        return values


class YandexAuth(OpenIdAuth):
    """Yandex OpenID authentication"""
    AUTH_BACKEND = YandexBackend
        
    def openid_url(self):
        """Returns Yandex authentication URL"""
        if YANDEX_USER_FIELD not in self.data:
            return YANDEX_OID_2_URL
        else:
            return YANDEX_URL % self.data[YANDEX_USER_FIELD]
    
# Backend definition
BACKENDS = {
    'yandex': YandexAuth,
}

"""
Vkontakte OAuth support.

"""
from urllib import urlencode, urlopen

from django.utils import simplejson

from social_auth.utils import setting
from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME


# Vkontakte configuration
VK_AUTHORIZATION_URL = 'http://oauth.vk.com/authorize'
VK_ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
VK_USER_DATA_URL = 'https://api.vk.com/method/users.get'
VK_SERVER = 'vk.com'


class VkontakteBackend(OAuthBackend):
    """Vkontakte OAuth authentication backend"""
    name = 'vkontakte'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_id(self, details, response):
        "OAuth providers return an unique user id in response"""
        return response['user_id']

    def get_user_details(self, response):
        """Return user details from Vkontakte account"""
        print response
        return {USERNAME: response.get('nickname') or \
                          response.get('screen_name'),
                'email':  '',
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name')}


class VkontakteAuth(BaseOAuth2):
    """Vkontakte OAuth mechanism"""
    AUTHORIZATION_URL = VK_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = VK_ACCESS_TOKEN_URL
    SERVER_URL = VK_SERVER
    AUTH_BACKEND = VkontakteBackend
    SETTINGS_KEY_NAME = 'VK_APP_ID'
    SETTINGS_SECRET_NAME = 'VK_API_SECRET'

    def user_data(self, access_token, response, *args, **kwargs):
        """Loads user data from service"""
        params = {'access_token': access_token,
                  'fields': 'first_name,last_name,screen_name,nickname',
                  'uids': response.get('user_id')
                 }
        url = VK_USER_DATA_URL + '?' + urlencode(params)
        try:
            return simplejson.load(urlopen(url)).get('response')[0]
        except (ValueError, IndexError):
            return None

    def get_scope(self):
        """Return list with needed access scope"""
        # Look at http://vk.com/developers.php?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
        return setting('VK_EXTRA_SCOPE', [])


# Backend definition
BACKENDS = {
    'vkontakte': VkontakteAuth,
}

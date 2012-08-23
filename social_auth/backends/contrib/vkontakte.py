# -*- coding: utf-8 -*-
"""
VKontakte OpenAPI and OAuth 2.0 support.

This contribution adds support for VKontakte OpenAPI and OAuth 2.0 service in
the form www.vkontakte.ru. Username is retrieved from the identity returned by
server.
"""

from django.contrib.auth import authenticate
from django.utils import simplejson

from urllib import urlencode
from hashlib import md5
from time import time

from social_auth.backends import SocialAuthBackend, OAuthBackend, BaseAuth, \
                                 BaseOAuth2, USERNAME
from social_auth.utils import setting, log, dsa_urlopen


# Vkontakte configuration
VK_AUTHORIZATION_URL = 'http://oauth.vk.com/authorize'
VK_ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
VK_SERVER = 'vk.com'
VK_DEFAULT_DATA = ['first_name', 'last_name', 'screen_name',
                   'nickname', 'photo']

VKONTAKTE_API_URL = 'https://api.vkontakte.ru/method/'
VKONTAKTE_SERVER_API_URL = 'http://api.vkontakte.ru/api.php'
VKONTAKTE_API_VERSION = '3.0'

USE_APP_AUTH = setting('VKONTAKTE_APP_AUTH', False)
LOCAL_HTML = setting('VKONTAKTE_LOCAL_HTML', 'vkontakte.html')


class VKontakteBackend(SocialAuthBackend):
    """VKontakte OpenAPI authentication backend"""
    name = 'vkontakte'

    def get_user_id(self, details, response):
        """Return user unique id provided by VKontakte"""
        return response['id']

    def get_user_details(self, response):
        """Return user details from VKontakte request"""
        nickname = response.get('nickname') or ''
        return {
            USERNAME: response['id'] if len(nickname) == 0 else nickname,
            'email': '',
            'fullname': '',
            'first_name': response.get('first_name')[0]
                                if 'first_name' in response else '',
            'last_name': response.get('last_name')[0]
                                if 'last_name' in response else ''
        }


class VKontakteAuth(BaseAuth):
    """VKontakte OpenAPI authorization mechanism"""
    AUTH_BACKEND = VKontakteBackend
    APP_ID = setting('VKONTAKTE_APP_ID')

    def user_data(self, access_token, *args, **kwargs):
        return dict(self.request.GET)

    def auth_html(self):
        """Returns local VK authentication page, not necessary for
        VK to authenticate.
        """
        from django.template import RequestContext, loader

        dict = {'VK_APP_ID': self.APP_ID,
                'VK_COMPLETE_URL': self.redirect}

        vk_template = loader.get_template(LOCAL_HTML)
        context = RequestContext(self.request, dict)

        return vk_template.render(context)

    def auth_complete(self, *args, **kwargs):
        """Performs check of authentication in VKontakte, returns User if
        succeeded"""
        app_cookie = 'vk_app_' + self.APP_ID

        if not 'id' in self.request.GET or \
           not app_cookie in self.request.COOKIES:
            raise ValueError('VKontakte authentication is not completed')

        cookie_dict = dict(item.split('=') for item in
                                self.request.COOKIES[app_cookie].split('&'))
        check_str = ''.join(item + '=' + cookie_dict[item]
                                for item in ['expire', 'mid', 'secret', 'sid'])

        hash = md5(check_str + setting('VKONTAKTE_APP_SECRET')).hexdigest()

        if hash != cookie_dict['sig'] or int(cookie_dict['expire']) < time():
            raise ValueError('VKontakte authentication failed: invalid hash')
        else:
            kwargs.update({
                'auth': self,
                'response': self.user_data(cookie_dict['mid']),
                self.AUTH_BACKEND.name: True
            })
            return authenticate(*args, **kwargs)

    @property
    def uses_redirect(self):
        """VKontakte does not require visiting server url in order
        to do authentication, so auth_xxx methods are not needed to be called.
        Their current implementation is just an example"""
        return False


class VKontakteOAuth2Backend(OAuthBackend):
    """VKontakteOAuth2 authentication backend"""
    name = 'vkontakte-oauth2'

    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_id(self, details, response):
        """OAuth providers return an unique user id in response"""
        return response['user_id']

    def get_user_details(self, response):
        """Return user details from Vkontakte account"""
        return {
            USERNAME: response.get('screen_name'),
            'email':  '',
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name')
        }


class VKontakteOAuth2(BaseOAuth2):
    """Vkontakte OAuth mechanism"""
    AUTHORIZATION_URL = VK_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = VK_ACCESS_TOKEN_URL
    SERVER_URL = VK_SERVER
    AUTH_BACKEND = VKontakteOAuth2Backend
    SETTINGS_KEY_NAME = 'VK_APP_ID'
    SETTINGS_SECRET_NAME = 'VK_API_SECRET'
    # Look at:
    # http://vk.com/developers.php?oid=-17680044&p=Application_Access_Rights
    SCOPE_VAR_NAME = 'VK_EXTRA_SCOPE'

    def get_scope(self):
        return setting(VKontakteOAuth2.SCOPE_VAR_NAME) or \
               setting('VKONTAKTE_OAUTH2_EXTRA_SCOPE')

    def user_data(self, access_token, response, *args, **kwargs):
        """Loads user data from service"""
        fields = ','.join(VK_DEFAULT_DATA + setting('VK_EXTRA_DATA', []))
        params = {'access_token': access_token,
                  'fields': fields,
                  'uids': response.get('user_id')}

        data = vkontakte_api('users.get', params)

        if data:
            data = data.get('response')[0]
            data['user_photo'] = data.get('photo')  # Backward compatibility

        return data


class VKontakteAppAuth(VKontakteOAuth2):
    """VKontakte Application Authentication support"""

    def auth_complete(self, *args, **kwargs):
        if USE_APP_AUTH:
            stop, app_auth = self.application_auth(*args, **kwargs)

            if app_auth:
                return app_auth

            if stop:
                return None

        return super(VKontakteAppAuth, self).auth_complete(*args, **kwargs)

    def user_profile(self, user_id, access_token=None):
        data = {'uids': user_id, 'fields': 'photo'}

        if access_token:
            data['access_token'] = access_token

        profiles = vkontakte_api('getProfiles', data).get('response', None)

        return profiles[0] if profiles else None

    def is_app_user(self, user_id, access_token=None):
        """Returns app usage flag from VKontakte API"""

        data = {'uid': user_id}

        if access_token:
            data['access_token'] = access_token

        return vkontakte_api('isAppUser', data).get('response', 0)

    def application_auth(self, *args, **kwargs):
        required_params = ('is_app_user', 'viewer_id', 'access_token',
                           'api_id')

        for param in required_params:
            if not param in self.request.REQUEST:
                return (False, None)

        auth_key = self.request.REQUEST.get('auth_key')

        # Verify signature, if present
        if auth_key:
            check_key = md5('_'.join([self.request.REQUEST.get('api_id'),
                                  self.request.REQUEST.get('viewer_id'),
                                  USE_APP_AUTH['key']])).hexdigest()

            if check_key != auth_key:
                raise ValueError('VKontakte authentication failed: invalid '
                                 'auth key')

        user_check = USE_APP_AUTH.get('user_mode', 0)
        user_id = self.request.REQUEST.get('viewer_id')

        if user_check:
            is_user = self.request.REQUEST.get('is_app_user') \
                        if user_check == 1 else self.is_app_user(user_id)

            if not int(is_user):
                return (True, None)

        data = {'response': self.user_profile(user_id), 'user_id': user_id}

        return (True, authenticate(*args, **{'auth': self,
            'request': self.request,
            'response': data, self.AUTH_BACKEND.name: True
        }))


def _api_get_val_fun(name, conf):
    if USE_APP_AUTH:
        return USE_APP_AUTH.get(name)
    else:
        return setting(conf)


def vkontakte_api(method, data):
    """Calls VKontakte OpenAPI method
        http://vkontakte.ru/apiclub,
        http://vkontakte.ru/pages.php?o=-1&p=%C2%FB%EF%EE%EB%ED%E5%ED%E8%E5%20
                                             %E7%E0%EF%F0%EE%F1%EE%E2%20%EA%20
                                             API
    """

    # We need to perform server-side call if no access_token
    if not 'access_token' in data:
        if not 'v' in data:
            data['v'] = VKONTAKTE_API_VERSION

        if not 'api_id' in data:
            data['api_id'] = _api_get_val_fun('id', 'VKONTAKTE_APP_ID')

        data['method'] = method
        data['format'] = 'json'

        url = VKONTAKTE_SERVER_API_URL
        secret = _api_get_val_fun('key', 'VKONTAKTE_APP_SECRET')

        param_list = sorted(list(item + '=' + data[item] for item in data))
        data['sig'] = md5(''.join(param_list) + secret).hexdigest()
    else:
        url = VKONTAKTE_API_URL + method

    params = urlencode(data)
    url += '?' + params
    try:
        return simplejson.load(dsa_urlopen(url))
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        log('error', 'Could not load data from VKontakte.',
            exc_info=True, extra=dict(data=data))
        return None


# Backend definition
BACKENDS = {
    'vkontakte': VKontakteAuth,
    'vkontakte-oauth2': VKontakteAppAuth if USE_APP_AUTH else VKontakteOAuth2
}

"""
VKontakte OpenAPI and OAuth 2.0 support.

This contribution adds support for VKontakte OpenAPI and OAuth 2.0 service in the form
www.vkontakte.ru. Username is retrieved from the identity returned by server.
"""

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import simplejson

from urllib import urlencode, unquote
from urllib2 import Request, urlopen, HTTPError
from hashlib import md5
from time import time

from social_auth.backends import SocialAuthBackend, OAuthBackend, BaseAuth, BaseOAuth2, USERNAME

VKONTAKTE_API_URL        = 'https://api.vkontakte.ru/method/'
VKONTAKTE_SERVER_API_URL = 'http://api.vkontakte.ru/api.php'
VKONTAKTE_API_VERSION    = '3.0'

VKONTAKTE_OAUTH2_SCOPE  = [''] # Enough for authentication

EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')
USE_APP_AUTH = getattr(settings, 'VKONTAKTE_APP_AUTH', False)
LOCAL_HTML = getattr(settings, 'VKONTAKTE_LOCAL_HTML', 'vkontakte.html')

class VKontakteBackend(SocialAuthBackend):
    """VKontakte authentication backend"""
    name = 'vkontakte'

    def get_user_id(self, details, response):
        """Return user unique id provided by VKontakte"""
        return int(response.GET['id'])

    def get_user_details(self, response):
        """Return user details from VKontakte request"""
        nickname = unquote(response.GET['nickname'])
        values = { USERNAME: response.GET['id'] if len(nickname) == 0 else nickname, 'email': '', 'fullname': '',
                  'first_name': unquote(response.GET['first_name']), 'last_name': unquote(response.GET['last_name'])}
        return values


class VKontakteOAuth2Backend(OAuthBackend):
    """VKontakteOAuth2 authentication backend"""
    name = 'vkontakte-oauth2'
    EXTRA_DATA = [('expires_in', EXPIRES_NAME)]

    def get_user_id(self, details, response):
        """Return user unique id provided by VKontakte"""
        return int(response['user_id'])

    def get_user_details(self, response):
        """Return user details from VKontakte request"""
        values = { USERNAME: str(response['user_id']), 'email': ''}

        details = response['response']
        user_name = details.get('user_name')

        if user_name:
            values['fullname'] = unquote(user_name)

            if ' ' in values['fullname']:
                values['first_name'], values['last_name'] = values['fullname'].split()
            else:
                values['first_name'] = values['fullname']

        if 'last_name' in details:
            values['last_name'] = unquote(details['last_name'])

        if 'first_name' in details:
            values['first_name'] = unquote(details['first_name'])

        return values


class VKontakteAuth(BaseAuth):
    """VKontakte OpenAPI authorization mechanism"""
    AUTH_BACKEND = VKontakteBackend
    APP_ID = settings.VKONTAKTE_APP_ID

    def auth_html(self):
        """Returns local VK authentication page, not necessary for VK to authenticate """
        from django.core.urlresolvers import reverse
        from django.template import RequestContext, loader

        dict = { 'VK_APP_ID'      : self.APP_ID,
                 'VK_COMPLETE_URL': reverse(settings.SOCIAL_AUTH_COMPLETE_URL_NAME, args=[VKontakteBackend.name]) }

        vk_template = loader.get_template(LOCAL_HTML)
        context = RequestContext(self.request, dict)

        return vk_template.render(context)

    def auth_complete(self, *args, **kwargs):
        """Performs check of authentication in VKontakte, returns User if succeeded"""
        app_cookie = 'vk_app_' + self.APP_ID

        if not 'id' in self.request.GET or not app_cookie in self.request.COOKIES:
            raise ValueError('VKontakte authentication is not completed')

        cookie_dict = dict(item.split('=') for item in self.request.COOKIES[app_cookie].split('&'))
        check_str = ''.join([item + '=' + cookie_dict[item] for item in ['expire', 'mid', 'secret', 'sid']])

        hash = md5(check_str + settings.VKONTAKTE_APP_SECRET).hexdigest()

        if hash != cookie_dict['sig'] or int(cookie_dict['expire']) < time() :
            raise ValueError('VKontakte authentication failed: invalid hash')
        else:
            kwargs.update({'response': self.request, self.AUTH_BACKEND.name: True})
            return authenticate(*args, **kwargs)

    @property
    def uses_redirect(self):
        """VKontakte does not require visiting server url in order
        to do authentication, so auth_xxx methods are not needed to be called.
        Their current implementation is just an example"""
        return False


class VKontakteOAuth2(BaseOAuth2):
    """VKontakte OAuth2 support"""
    AUTH_BACKEND = VKontakteOAuth2Backend
    AUTHORIZATION_URL = 'http://api.vkontakte.ru/oauth/authorize'
    ACCESS_TOKEN_URL = ' https://api.vkontakte.ru/oauth/access_token'
    SETTINGS_KEY_NAME = 'VKONTAKTE_APP_ID'
    SETTINGS_SECRET_NAME = 'VKONTAKTE_APP_SECRET'

    def get_scope(self):
        return VKONTAKTE_OAUTH2_SCOPE + getattr(settings, 'VKONTAKTE_OAUTH2_EXTRA_SCOPE', [])

    def auth_complete(self, *args, **kwargs):
        if USE_APP_AUTH:
            stop, app_auth = self.application_auth()

            if app_auth:
                return app_auth

            if stop:
                return None

        try:
            auth_result = super(VKontakteOAuth2, self).auth_complete(*args, **kwargs)
        except HTTPError: # VKontakte returns HTTPError 400 if cancelled
            raise ValueError('Authentication cancelled')

        return auth_result

    def user_data(self, access_token):
        """Return user data from VKontakte API"""
        data = {'access_token': access_token }

        return vkontakte_api('getUserInfoEx', data)

    def user_profile(self, user_id, access_token = None):
        data = {'uids': user_id, 'fields': 'photo'}

        if access_token:
            data['access_token'] = access_token

        profiles = vkontakte_api('getProfiles', data).get('response', None)

        return profiles[0] if profiles else None

    def is_app_user(self, user_id, access_token = None):
        """Returns app usage flag from VKontakte API"""

        data = {'uid': user_id}

        if access_token:
            data['access_token'] = access_token

        return vkontakte_api('isAppUser', data).get('response', 0)

    def application_auth(self):
        required_params = ('is_app_user', 'viewer_id', 'access_token', 'api_id', )

        for param in required_params:
            if not param in self.request.REQUEST:
                return (False, None,)

        auth_key = self.request.REQUEST.get('auth_key')

        # Verify signature, if present
        if auth_key:
            check_key = md5(self.request.REQUEST.get('api_id') + '_' + self.request.REQUEST.get('viewer_id') + '_' + \
                            USE_APP_AUTH['key']).hexdigest()
            if check_key != auth_key:
                raise('VKontakte authentication failed: invalid auth key')

        user_check = USE_APP_AUTH.get('user_mode', 0)
        user_id = self.request.REQUEST.get('viewer_id')

        if user_check:
            is_user = self.request.REQUEST.get('is_app_user') if user_check == 1 else self.is_app_user(user_id)

            if not int(is_user):
                return (True, None,)

        data = {'response': self.user_profile(user_id), 'user_id': user_id}

        return (True, authenticate(**{'response': data, self.AUTH_BACKEND.name: True}))


def vkontakte_api(method, data):
    """ Calls VKontakte OpenAPI method
        http://vkontakte.ru/apiclub,
        http://vkontakte.ru/pages.php?o=-1&p=%C2%FB%EF%EE%EB%ED%E5%ED%E8%E5%20%E7%E0%EF%F0%EE%F1%EE%E2%20%EA%20API
    """

    # We need to perform server-side call if no access_token
    if not 'access_token' in data:
        if not 'v' in data:
            data['v'] = VKONTAKTE_API_VERSION

        if not 'api_id' in data:
            data['api_id'] = USE_APP_AUTH.get('id') if USE_APP_AUTH else settings.VKONTAKTE_APP_ID

        data['method'] = method
        data['format'] = 'json'

        url = VKONTAKTE_SERVER_API_URL
        secret = USE_APP_AUTH.get('key') if USE_APP_AUTH else settings.VKONTAKTE_APP_SECRET

        param_list = sorted(list(item + '=' + data[item] for item in data))
        data['sig'] = md5(''.join(param_list) + secret).hexdigest()
    else:
        url = VKONTAKTE_API_URL + method

    params = urlencode(data)
    api_request = Request(url + '?' + params)
    try:
        return simplejson.loads(urlopen(api_request).read())
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        return None


# Backend definition
BACKENDS = {
    'vkontakte': VKontakteAuth,
    'vkontakte-oauth2': VKontakteOAuth2
}

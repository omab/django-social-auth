"""
VKontakte OpenAPI and OAuth 2.0 support.

This contribution adds support for VKontakte OpenAPI and OAuth 2.0 service in the form
www.vkontakte.ru. Username is retrieved from the identity returned by server.
"""

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import simplejson

from urllib import urlencode, unquote
from urllib2 import Request, urlopen
from hashlib import md5
from time import time

from social_auth.backends import SocialAuthBackend, OAuthBackend, BaseAuth, BaseOAuth2, USERNAME

VKONTAKTE_LOCAL_HTML  = 'vkontakte.html'

VKONTAKTE_API_URL       = 'https://api.vkontakte.ru/method/'
VKONTAKTE_OAUTH2_SCOPE  = [''] # Enough for authentication

EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')
USE_APP_AUTH = getattr(settings, 'VKONTAKTE_APP_AUTH', False)

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
        values = { USERNAME: str(response['user_id']), 'email': '', 'fullname': unquote(response['response']['user_name']),
                  'first_name': '', 'last_name': ''}
        
        if ' ' in values['fullname']:
            values['first_name'], values['last_name'] = values['fullname'].split()
        else:
            values['first_name'] = values['fullname']
            
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
        
        vk_template = loader.get_template(VKONTAKTE_LOCAL_HTML)
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

        return super(VKontakteOAuth2, self).auth_complete(*args, **kwargs)

    def user_data(self, access_token):
        """Return user data from VKontakte OpenAPI"""
        data = {'access_token': access_token }
        
        return vkontakte_api('getUserInfoEx', data)

    def application_auth(self):
        required_params = ('is_app_user', 'viewer_id', 'access_token', 'api_id', )

        for param in required_params:
            if not param in self.request.REQUEST:
                return (False, None,)

        is_user = self.request.REQUEST.get('is_app_user')

        if not int(is_user):
            return (True, None,)

        auth_key = self.request.REQUEST.get('auth_key')

        # Verify signature, if present
        if auth_key:
            check_key = md5(self.request.REQUEST.get('api_id') + '_' + self.request.REQUEST.get('viewer_id') + '_' + \
                            USE_APP_AUTH).hexdigest()
            if check_key != auth_key:
                raise('VKontakte authentication failed: invalid auth key')

        access_token = self.request.REQUEST.get('access_token')

        data = self.user_data(access_token)
        data['user_id'] = self.request.REQUEST.get('viewer_id')
        data['access_token'] = access_token
        data['secret'] = self.request.REQUEST.get('secret')

        return (True, authenticate(**{'response': data, self.AUTH_BACKEND.name: True}))


def vkontakte_api(method, data):
    """ Calls VKontakte OpenAPI method
        http://vkontakte.ru/apiclub, 
        http://vkontakte.ru/pages.php?o=-1&p=%C2%FB%EF%EE%EB%ED%E5%ED%E8%E5%20%E7%E0%EF%F0%EE%F1%EE%E2%20%EA%20API
    """

    params = urlencode(data)
    request = Request(VKONTAKTE_API_URL + method + '?' + params)
    try:
        return simplejson.loads(urlopen(request).read())
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        return None
        
# Backend definition
BACKENDS = {
    'vkontakte': VKontakteAuth,
    'vkontakte-oauth2': VKontakteOAuth2
}
    

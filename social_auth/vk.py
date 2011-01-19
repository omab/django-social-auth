from django.conf import settings
from django.contrib.auth import authenticate
from urllib import unquote
import md5

from backends import SocialAuthBackend, USERNAME
from auth import BaseAuth, BACKENDS


class VKontakteBackend(SocialAuthBackend):
    """VKontakte authentication backend"""
    name = 'vkontakte'

    def get_user_id(self, details, response):
        """Return user unique id provided by VKontakte"""
        return int(response.GET['id'])
    
    def get_user_details(self, response):
        """Return user details from VKontakte request"""
        values = { USERNAME: unquote(response.GET['nickname']), 'email': '', 'fullname': '',
                  'first_name': unquote(response.GET['first_name']), 'last_name': unquote(response.GET['last_name'])}
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
                 'VK_COMPLETE_URL': reverse('social:complete', args=[VKontakteBackend.name]) }
        
        vk_template = loader.get_template(settings.VKONTAKTE_LOCAL_HTML)
        context = RequestContext(self.request, dict)
    
        return vk_template.render(context)
        
    def auth_complete(self, *args, **kwargs):
        """Performs check of authentication in VKontakte, returns User if succeeded"""
        app_cookie = 'vk_app_' + self.APP_ID
        
        if not 'id' in self.request.GET or not app_cookie in self.request.COOKIES:
            raise ValueError('VKontakte authentication is not completed')
        
        cookie_dict = dict(item.split('=') for item in self.request.COOKIES[app_cookie].split('&'))
        check_str = ''.join([item + '=' + cookie_dict[item] for item in ['expire', 'mid', 'secret', 'sid']])
        
        hash = md5.new(check_str + settings.VKONTAKTE_APP_SECRET).hexdigest()
        
        if hash != cookie_dict['sig']:
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
    
    
def add_VK_Auth():
    BACKENDS[VKontakteBackend.name] = VKontakteAuth
    

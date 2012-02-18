"""
Google App Engine support using User API
"""
from __future__ import absolute_import

from django.contrib.auth import authenticate

from social_auth.backends import SocialAuthBackend, BaseAuth, USERNAME

from google.appengine.api import users

class GAEBackend(SocialAuthBackend):
    """BrowserID authentication backend"""
    name = 'GAE'

    def get_user_id(self, details, response):
        """Use BrowserID email as ID"""
        user = users.get_current_user()
        if user:
            return user.user_id()

    def get_user_details(self, response):
        """Return user details, BrowserID only provides Email."""
        # {'status': 'okay',
        #  'audience': 'localhost:8000',
        #  'expires': 1328983575529,
        #  'email': 'name@server.com',
        #  'issuer': 'browserid.org'}
        user = users.get_current_user()
        return {USERNAME: user.user_id(),
                'email': user.email(),
                'fullname': '',
                'first_name': '',
                'last_name': ''}

# Auth classes
class GAEAuth(BaseAuth):
    """BrowserID authentication"""
    AUTH_BACKEND = GAEBackend

    def auth_url(self):
        return users.create_login_url('/complete/gae')

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if not users.get_current_user():
            raise ValueError('Authentication error')

        """ Setting these two are necessary for BaseAuth.authenticate to work """
        kwargs.update({
            'response' : '',
            self.AUTH_BACKEND.name: True
        })

        return authenticate(*args, **kwargs)

# Backend definition
BACKENDS = {
    'gae': GAEAuth,
}

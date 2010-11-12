"""
Authentication backeds for django.contrib.auth AUTHENTICATION_BACKENDS setting
"""
from openid.extensions import ax, sreg

from .base import SocialAuthBackend
from .conf import OLD_AX_ATTRS, AX_SCHEMA_ATTRS


class OAuthBackend(SocialAuthBackend):
    """OAuth authentication backend base class"""
    def get_user_id(self, details, response):
        "OAuth providers return an unique user id in response"""
        return response['id']


class TwitterBackend(OAuthBackend):
    """Twitter OAuth authentication backend"""
    name = 'twitter'

    def authenticate(self, **kwargs):
        """Authenticate user only if this was a Twitter request"""
        if kwargs.pop('twitter', False):
            return super(TwitterBackend, self).authenticate(**kwargs)

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        return {'email': '', # not supplied
                'username': response['screen_name'],
                'fullname': response['name'],
                'firstname': response['name'],
                'lastname': ''}


class FacebookBackend(OAuthBackend):
    """Facebook OAuth authentication backend"""
    name = 'facebook'

    def authenticate(self, **kwargs):
        """Authenticate user only if this was a Facebook request"""
        if kwargs.pop('facebook', False):
            return super(FacebookBackend, self).authenticate(**kwargs)

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {'email': response.get('email', ''),
                'username': response['name'],
                'fullname': response['name'],
                'firstname': response.get('first_name', ''),
                'lastname': response.get('last_name', '')}

       
class OpenIDBackend(SocialAuthBackend):
    """Generic OpenID authentication backend"""
    name = 'openid'

    def authenticate(self, **kwargs):
        """Authenticate the user based on an OpenID response."""
        if kwargs.pop('openid', False):
            return super(OpenIDBackend, self).authenticate(**kwargs)

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return response.identity_url

    def get_user_details(self, response):
        """Return user details from an OpenID request"""
        values = {'email': '',
                  'username': '',
                  'fullname': '',
                  'firstname': '',
                  'lastname': ''}

        resp = sreg.SRegResponse.fromSuccessResponse(response)
        if resp:
            values.update((name, resp.get(name) or values.get(name) or '')
                                for name in ('email', 'fullname', 'nickname'))

        # Use Attribute Exchange attributes if provided
        resp = ax.FetchResponse.fromSuccessResponse(response)
        if resp:
            values.update((alias.replace('old_', ''), resp.getSingle(src))
                            for src, alias in OLD_AX_ATTRS + AX_SCHEMA_ATTRS)

        fullname = values.get('fullname') or ''
        firstname = values.get('firstname') or ''
        lastname = values.get('lastname') or ''

        if not fullname and firstname and lastname:
            fullname = firstname + ' ' + lastname
        elif fullname:
            try: # Try to split name for django user storage
                firstname, lastname = fullname.rsplit(' ', 1)
            except ValueError:
                lastname = fullname

        values.update({'fullname': fullname,
                       'firstname': firstname,
                       'lastname': lastname,
                       'username': values.get('username') or \
                                   (firstname.title() + lastname.title())})
        return values

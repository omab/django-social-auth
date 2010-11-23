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

    def extra_data(self, user, uid, response, details):
        """Return access_token to store in extra_data field"""
        return response.get('access_token', '')


class TwitterBackend(OAuthBackend):
    """Twitter OAuth authentication backend"""
    name = 'twitter'

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        return {'email': '', # not supplied
                'username': response['screen_name'],
                'fullname': response['name'],
                'first_name': response['name'],
                'last_name': ''}


class OrkutBackend(OAuthBackend):
    """Orkut OAuth authentication backend"""
    name = 'orkut'

    def get_user_details(self, response):
        """Return user details from Orkut account"""
        return {'email': response['emails'][0]['value'],
                'username': response['displayName'],
                'fullname': response['displayName'],
                'firstname': response['name']['givenName'],
                'lastname': response['name']['familyName']}


class FacebookBackend(OAuthBackend):
    """Facebook OAuth authentication backend"""
    name = 'facebook'

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {'email': response.get('email', ''),
                'username': response['name'],
                'fullname': response['name'],
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}

       
class OpenIDBackend(SocialAuthBackend):
    """Generic OpenID authentication backend"""
    name = 'openid'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return response.identity_url

    def get_user_details(self, response):
        """Return user details from an OpenID request"""
        values = {'email': '',
                  'username': '',
                  'fullname': '',
                  'first_name': '',
                  'last_name': ''}

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
        first_name = values.get('first_name') or ''
        last_name = values.get('last_name') or ''

        if not fullname and first_name and last_name:
            fullname = first_name + ' ' + last_name
        elif fullname:
            try: # Try to split name for django user storage
                first_name, last_name = fullname.rsplit(' ', 1)
            except ValueError:
                last_name = fullname

        values.update({'fullname': fullname,
                       'first_name': first_name,
                       'last_name': last_name,
                       'username': values.get('username') or \
                                   (first_name.title() + last_name.title())})
        return values

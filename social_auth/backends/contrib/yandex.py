"""
Yandex OpenID support.

This contribution adds support for Yandex.ru OpenID service in the form
openid.yandex.ru/user. Username is retrieved from the identity url.

If username is not specified, OpenID 2.0 url used for authentication.
"""
import logging
logger = logging.getLogger(__name__)

import urlparse

from urllib import urlencode, unquote
from urllib2 import Request, urlopen, HTTPError

from django.conf import settings
import xml.dom.minidom

from social_auth.backends import OpenIDBackend, OpenIdAuth, USERNAME, OAuthBackend, BaseOAuth2


# Yandex conf
YANDEX_URL = 'http://openid.yandex.ru/%s'
YANDEX_USER_FIELD = 'openid_ya_user'
YANDEX_OID_2_URL = 'http://yandex.ru'

EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')

class YandexBackend(OpenIDBackend):
    """Yandex OpenID authentication backend"""
    name = 'yandex'

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super(YandexBackend, self).get_user_details(response)
        values[USERNAME] = values.get(USERNAME) or \
                           urlparse.urlsplit(response.identity_url)\
                                   .path.strip('/')

        values['email'] = values.get('email') or ''

        return values


class YandexOAuth2Backend(OAuthBackend):
    """Yandex OAuth2 authentication backend"""
    name = 'yandex-oauth2'

    def get_user_id(self, details, response):
        """Return user unique id provided by Yandex"""
        return int(response['id'])

    def get_user_details(self, response):
        """Return user details from Yandex request"""

        name = unquote(response['name'])
        first_name = ''
        last_name = ''

        if ' ' in name:
            last_name, first_name = name.split(' ')
            name = first_name
        else:
            first_name = name

        values = { USERNAME: name, 'email': '',
                   'first_name': first_name, 'last_name': last_name}

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


class YandexOAuth2(BaseOAuth2):
    """Yandex OAuth2 support
       See http://api.yandex.ru/oauth/doc/dg/concepts/About.xml for details"""
    AUTH_BACKEND = YandexOAuth2Backend
    AUTHORIZATION_URL = 'https://oauth.yandex.ru/authorize'
    ACCESS_TOKEN_URL = 'https://oauth.yandex.ru/token'
    SETTINGS_KEY_NAME = 'YANDEX_OAUTH2_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'YANDEX_OAUTH2_CLIENT_SECRET'

    def get_scope(self):
        return [] # Yandex does not allow custom scope

    def auth_complete(self, *args, **kwargs):
        try:
            auth_result = super(YandexOAuth2, self).auth_complete(*args, **kwargs)
        except HTTPError: # Returns HTTPError 400 if cancelled
            raise ValueError('Authentication cancelled')

        return auth_result

    def user_data(self, access_token):
        """Return user data from Yandex REST API specified in settings"""
        params = urlencode({'text': 1, 'format': 'xml'})
        request = Request(settings.YANDEX_OAUTH2_API_URL + '?' + params, headers={'Authorization': "OAuth " + access_token })

        try:
            dom = xml.dom.minidom.parseString(urlopen(request).read())

            id = getNodeText(dom, "id")
            if "/" in id:
                id = id.split("/")[-1]

            name = getNodeText(dom, "name")

            links = getNodesWithAttribute(dom, "link", {"rel": "userpic"})
            userpic = links[0].getAttribute("href") if links else ""

            return {"id": id, "name": name, "userpic": userpic, "access_token": access_token}
        except (TypeError, KeyError, IOError, ValueError, IndexError):
            logger.error('Could not load data from Yandex.', exc_info=True, extra=dict(data=params))
            return None


def getNodeText(dom, nodeName):
    nodelist = dom.getElementsByTagName(nodeName)[0].childNodes

    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)

    return ''.join(rc)

def getNodesWithAttribute(dom, nodeName, attrDict):
    nodelist = dom.getElementsByTagName(nodeName)
    found = []

    for node in nodelist:
        for key, value in attrDict.items():
            if node.hasAttribute(key):
                if value and node.getAttribute(key) != value:
                    continue
                found.append(node)

    return found

# Backend definition
BACKENDS = {
    'yandex': YandexAuth,
    'yandex-oauth2': YandexOAuth2
}

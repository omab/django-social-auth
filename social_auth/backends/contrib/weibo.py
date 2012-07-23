#coding:utf8
#author:hepochen@gmail.com  https://github.com/hepochen
"""
Weibo OAuth2 support.

This script adds support for Weibo OAuth service. An application must
be registered first on http://open.weibo.com.

WEIBO_CLIENT_KEY and WEIBO_CLIENT_SECRET must be defined in the settings.py
correctly.

By default account id,profile_image_url,gender are stored in extra_data field,
check OAuthBackend class for details on how to extend it.
"""
from urllib import urlencode, urlopen

from django.utils import simplejson

from social_auth.backends import OAuthBackend, USERNAME, BaseOAuth2


WEIBO_SERVER = 'api.weibo.com'
WEIBO_REQUEST_TOKEN_URL = 'https://%s/oauth2/request_token' % WEIBO_SERVER
WEIBO_ACCESS_TOKEN_URL = 'https://%s/oauth2/access_token' % WEIBO_SERVER
WEIBO_AUTHORIZATION_URL = 'https://%s/oauth2/authorize' % WEIBO_SERVER


class WeiboBackend(OAuthBackend):
    """Weibo (of sina) OAuth authentication backend"""
    name = 'weibo'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('profile_image_url', 'profile_image_url'),
        ('gender', 'gender')
    ]

    def get_user_id(self, details, response):
        return response['uid']

    def get_user_details(self, response):
        """Return user details from Weibo. API URL is:
        https://api.weibo.com/2/users/show.json/?uid=<UID>&access_token=<TOKEN>
        """
        return {USERNAME: response["name"],
                'first_name': response.get('screen_name', '')}


class WeiboAuth(BaseOAuth2):
    """Douban OAuth authentication mechanism"""
    AUTHORIZATION_URL = WEIBO_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = WEIBO_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = WEIBO_ACCESS_TOKEN_URL
    SERVER_URL = WEIBO_SERVER
    AUTH_BACKEND = WeiboBackend
    SETTINGS_KEY_NAME = 'WEIBO_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'WEIBO_CLIENT_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        uid = args[0]['uid']
        url = 'https://api.weibo.com/2/users/show.json'
        data = {'access_token': access_token, 'uid': uid}
        c = urlopen(url + '?' + urlencode(data)).read()
        try:
            return simplejson.loads(c)
        except (ValueError, KeyError, IOError):
            return None


# Backend definition
BACKENDS = {
    'weibo': WeiboAuth
}

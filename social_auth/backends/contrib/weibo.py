#coding:utf8
#author:hepochen@gmail.com  https://github.com/hepochen
from django.utils import simplejson
from social_auth.backends import OAuthBackend, USERNAME, BaseOAuth2
from urllib import urlencode,urlopen

Weibo_SERVER = 'api.weibo.com'
Weibo_REQUEST_TOKEN_URL = 'https://%s/oauth2/request_token' %  Weibo_SERVER
Weibo_ACCESS_TOKEN_URL = 'https://%s/oauth2/access_token' %  Weibo_SERVER
Weibo_AUTHORIZATION_URL = 'https://%s/oauth2/authorize' % Weibo_SERVER


class WeiboBackend(OAuthBackend):
    """Weibo (of sina) OAuth authentication backend"""
    name = 'weibo'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('profile_image_url','profile_image_url'),
        ('gender','gender')
    ]

    def get_user_id(self, details, response):
        return response['uid']

    def get_user_details(self, response):
        """Return user details from Douban"""
        return {USERNAME: response["name"],
                'first_name': response.get('screen_name','')}


class WeiboAuth(BaseOAuth2):
    """Douban OAuth authentication mechanism"""
    AUTHORIZATION_URL = Weibo_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = Weibo_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = Weibo_ACCESS_TOKEN_URL
    SERVER_URL = Weibo_SERVER
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
    'weibo': WeiboAuth,
    }

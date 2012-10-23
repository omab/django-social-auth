"""
Yammer OAuth2 support
"""
from urllib import urlencode
from urlparse import parse_qs
import logging

from django.utils import simplejson
from django.utils.datastructures import MergeDict

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.backends.exceptions import AuthCanceled
from social_auth.utils import dsa_urlopen, setting

YAMMER_OAUTH_URL = 'https://www.yammer.com/oauth2/'
YAMMER_AUTH_URL = 'https://www.yammer.com/dialog/oauth'
YAMMER_API_URL = 'https://www.yammer.com/api/v1/'

class YammerBackend(OAuthBackend):
    name = 'yammer'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', setting('SOCIAL_AUTH_EXPIRATION', 'expires'))
    ]

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        """Reponse contains:
        {

            u'access_token': {
                u'user_id': 1490048335, 
                u'view_groups': True, 
                u'modify_messages': True,
                u'network_id': 477711,
                u'created_at': u'2012/10/23 04:43:15 +0000',
                u'view_members': True,
                u'authorized_at': u'2012/10/23 04:43:15 +0000',
                u'expires_at': None,
                u'view_messages': True,
                u'modify_subscriptions': True,
                u'token': u'xVZoNCKhWmg8xUfHLp2W4A',
                u'network_permalink': u'happiily.com',
                u'view_subscriptions': True,
                u'view_tags': True,
                u'network_name': u'happiily.com'
            },
            
            u'user': {
                u'last_name': u'H',
                u'web_url': u'https://www.yammer.com/happiily.com/users/matt',
                u'expertise': None,
                u'full_name': u'Matt H',
                u'timezone': u'Pacific Time (US & Canada)',
                u'kids_names': None,
                u'guid': None,
                u'network_name': u'happiily.com',
                u'id': 1490048335,
                u'previous_companies': [],
                u'first_name': u'Matt',
                u'stats': {
                    u'following': 3,
                    u'followers': 3,
                    u'updates': 2
                },
                u'hire_date': None,
                u'state': u'active',
                u'location': None,
                u'department': u'Development',
                u'type': u'user',
                u'show_ask_for_photo': True,
                u'job_title': u'fungineer',
                u'interests': None,
                u'mugshot_url': u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png',
                u'activated_at': u'2012/10/15 23:06:05 +0000',
                u'verified_admin': u'false',
                u'can_broadcast': u'false',
                u'schools': [],
                u'admin': u'false',
                u'network_domains': [u'happiily.com'],
                u'name': u'matt',
                u'settings': {u'xdr_proxy': u'https://xdrproxy.yammer.com'},
                u'network_id': 477711,
                u'external_urls': [],
                u'summary': None,
                u'url': u'https://www.yammer.com/api/v1/users/1490048335',
                u'contact': {
                    u'phone_numbers': [],
                    u'im': {
                        u'username': u'',
                        u'provider': u''
                    },
                    u'email_addresses': [
                        {
                            u'type': u'primary',
                            u'address': u'matt@happiily.com'
                        }
                    ]
                },
                u'birth_date': u'',
                u'mugshot_url_template': u'https://mug0.assets-yammer.com/mugshot/images/{width}x{height}/no_photo.png',
                u'significant_other': None
            },

            u'network': {
                u'show_upgrade_banner': False,
                u'created_at': u'2012/10/15 23:05:09 +0000',
                u'permalink': u'happiily.com',
                u'is_org_chart_enabled': True,
                u'navigation_text_color': u'#FFFFFF',
                u'is_group_enabled': True,
                u'header_background_color': u'#396B9A',
                u'navigation_background_color': u'#38699F',
                u'profile_fields_config': {
                    u'enable_work_phone': True,
                    u'enable_mobile_phone': True,
                    u'enable_job_title': True
                },
                u'header_text_color': u'#FFFFFF',
                u'community': False,
                u'is_chat_enabled': True,
                u'web_url': u'https://www.yammer.com/happiily.com',
                u'paid': False,
                u'type': u'network',
                u'id': 477711,
                u'name': u'happiily.com'
            }
        }

        """
        logging.error(response)


        username = response['user']['name']
        first_name = response['user']['first_name']
        last_name = response['user']['last_name']
        full_name = response['user']['full_name']
        email = response['user']['contact']['email_addresses'][0]['address']

        user_data = {
            USERNAME: username,
            'email': email,
            'fullname': full_name,
            'first_name': first_name,
            'last_name': last_name
        }

        return user_data

class YammerOAuth2(BaseOAuth2):
    AUTH_BACKEND = YammerBackend
    AUTHORIZATION_URL = YAMMER_AUTH_URL
    ACCESS_TOKEN_URL = '%s%s' % (YAMMER_OAUTH_URL, 'access_token')
    REQUEST_TOKEN_URL = '%s%s' % (YAMMER_OAUTH_URL, 'request_token')

    SETTINGS_KEY_NAME = 'YAMMER_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'YAMMER_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Load user data from yammer"""
        # /users/[:id].json
        params = {
            'client_id': setting(self.SETTINGS_KEY_NAME, ''),
            'client_secret': setting(self.SETTINGS_SECRET_NAME, ''),
            'code': access_token
        }
        url = '%s?%s' % (self.ACCESS_TOKEN_URL, urlencode(params))
        try:
            return simplejson.load(dsa_urlopen(url))
        except Exception, e:
            logging.exception(e)
        return None
    
    def auth_complete(self, *args, **kwargs):
        """Yammer API is a little strange"""
        if 'error' in self.data:
            logging.error("%s: %s:\n%s" % (
                self.data('error'), self.data('error_reason'),
                self.data('error_description')
            ))
            raise AuthCanceled(self)
        # now we need to clean up the data params
        new_data = {}
        redirect_state = self.data.get('redirect_state')
        try:
            parts = redirect_state.split('?')
            new_data['redirect_state'] = parts[0]
            extra = parse_qs(parts[1])
            new_data['code'] = extra['code'][0]
            self.data = MergeDict(new_data)
        except Exception as e:
            logging.exception(e)

        return super(YammerOAuth2, self).auth_complete(*args, **kwargs)

BACKENDS = {
    'yammer': YammerOAuth2,
}


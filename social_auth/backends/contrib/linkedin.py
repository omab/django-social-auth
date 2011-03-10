"""
Linkedin OAuth support

No extra configurations are needed to make this work.
"""
import urlparse
from xml.etree import ElementTree

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend


LINKEDIN_SERVER = 'linkedin.com'
LINKEDIN_REQUEST_TOKEN_URL = 'https://api.%s/uas/oauth/requestToken' % \
                                    LINKEDIN_SERVER
LINKEDIN_ACCESS_TOKEN_URL = 'https://api.%s/uas/oauth/accessToken' % \
                                    LINKEDIN_SERVER
LINKEDIN_AUTHORIZATION_URL = 'https://www.%s/uas/oauth/authenticate' % \
                                    LINKEDIN_SERVER
LINKEDIN_CHECK_AUTH = 'https://api.%s/v1/people/~' % LINKEDIN_SERVER


class LinkedinBackend(OAuthBackend):
    """Linkedin OAuth authentication backend"""
    name = 'linkedin'

    def get_user_details(self, response):
        """Return user details from Linkedin account"""
        return {
            'first_name': response['first-name'],
            'last_name': response['last-name'],
            'email': '',  # not supplied
        }


class LinkedinAuth(ConsumerBasedOAuth):
    """Linkedin OAuth authentication mechanism"""
    AUTHORIZATION_URL = LINKEDIN_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = LINKEDIN_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = LINKEDIN_ACCESS_TOKEN_URL
    SERVER_URL = 'api.%s' % LINKEDIN_SERVER
    AUTH_BACKEND = LinkedinBackend
    SETTINGS_KEY_NAME = 'LINKEDIN_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'LINKEDIN_CONSUMER_SECRET'

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, LINKEDIN_CHECK_AUTH)
        raw_xml = self.fetch_response(request)
        try:
            xml = ElementTree.fromstring(raw_xml)
            data = _xml_to_dict(xml)
            url = data['site-standard-profile-request']['url']
            url = url.replace('&amp;', '&')
            data['id'] = urlparse.parse_qs(url)['key'][0]

            return data
        except (xml.parsers.expat.ExpatError, KeyError, IndexError):
            return None

    @classmethod
    def enabled(cls):
        return True


def _xml_to_dict(xml):
    """Convert xml structure to dict"""
    data = {}
    for child in xml.getchildren():
        if child.getchildren():
            data[child.tag] = _xml_to_dict(child)
        else:
            data[child.tag] = child.text

    return data


# Backend definition
BACKENDS = {
    'linkedin': LinkedinAuth,
}

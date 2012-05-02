"""
EverNote OAuth support

No extra configurations are needed to make this work.
"""
try:
    from urlparse import parse_qs
    parse_qs  # placate pyflakes
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs

from oauth2 import Token
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME


EVERNOTE_SERVER = "sandbox.evernote.com"
#EVERNOTE_SERVER = 'www.evernote.com'
EVERNOTE_REQUEST_TOKEN_URL = 'https://%s/oauth' % \
                                    EVERNOTE_SERVER
EVERNOTE_ACCESS_TOKEN_URL = 'https://%s/oauth' % \
                                    EVERNOTE_SERVER
EVERNOTE_AUTHORIZATION_URL = 'https://%s/OAuth.action' % \
                                    EVERNOTE_SERVER


class EvernoteBackend(OAuthBackend):
    """Evernote OAuth authentication backend"""
    name = 'evernote'
    #EXTRA_DATA = [('id', 'id'),
                  #('first-name', 'first_name'),
                  #('last-name', 'last_name')]

    def get_user_details(self, response):
        """Return user details from Evernote account"""
        """
        {'edam_expires': ['1367525289541'],
         'edam_noteStoreUrl': ['https://sandbox.evernote.com/shard/s1/notestore'],
         'edam_shard': ['s1'],
         'edam_userId': ['123841'],
         'edam_webApiUrlPrefix': ['https://sandbox.evernote.com/shard/s1/'],
         'oauth_token': ['S=s1:U=1e3c1:E=13e66dbee45:C=1370f2ac245:P=185:A=onereceipt:H=411443c5e8b20f8718ed382a19d4ae38']}
        """
        return {USERNAME: response["edam_userId"],
                'email': '',
                }

    def get_user_id(self, details, response):
        return response['edam_userId']


class EvernoteAuth(ConsumerBasedOAuth):
    """Evernote OAuth authentication mechanism"""
    AUTHORIZATION_URL = EVERNOTE_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = EVERNOTE_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = EVERNOTE_ACCESS_TOKEN_URL
    SERVER_URL = '%s' % EVERNOTE_SERVER
    AUTH_BACKEND = EvernoteBackend
    SETTINGS_KEY_NAME = 'EVERNOTE_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'EVERNOTE_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return access_token.user_info

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        response = self.fetch_response(request)
        params = parse_qs(response)

        # evernote sents a empty secret token, this way it doesn't fires up the
        # exception
        response = response.replace("oauth_token_secret=", "oauth_token_secret=None")
        token = Token.from_string(response)

        token.user_info = params
        return token

# Backend definition
BACKENDS = {
    'evernote': EvernoteAuth,
}

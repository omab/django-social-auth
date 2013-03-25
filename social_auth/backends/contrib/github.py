"""
GitHub OAuth support.

This contribution adds support for GitHub OAuth service. The settings
GITHUB_APP_ID and GITHUB_API_SECRET must be defined with the values
given by GitHub application registration process.

GITHUB_ORGANIZATION is an optional setting that will allow you to constrain
authentication to a given GitHub organization.

Extended permissions are supported by defining GITHUB_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from urllib import urlencode
from urllib2 import HTTPError

from django.utils import simplejson
from django.conf import settings

from social_auth.utils import dsa_urlopen
from social_auth.backends import BaseOAuth2, OAuthBackend


# GitHub configuration
GITHUB_AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_DATA_URL = 'https://api.github.com/user'

# GitHub organization configuration
GITHUB_ORGANIZATION_MEMBER_OF_URL = \
        'https://api.github.com/orgs/{org}/members/{username}'

GITHUB_SERVER = 'github.com'


class GithubBackend(OAuthBackend):
    """Github OAuth authentication backend"""
    name = 'github'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}


class GithubAuth(BaseOAuth2):
    """Github OAuth2 mechanism"""
    AUTHORIZATION_URL = GITHUB_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = GITHUB_ACCESS_TOKEN_URL
    AUTH_BACKEND = GithubBackend
    SETTINGS_KEY_NAME = 'GITHUB_APP_ID'
    SETTINGS_SECRET_NAME = 'GITHUB_API_SECRET'
    SCOPE_SEPARATOR = ','
    # Look at http://developer.github.com/v3/oauth/
    SCOPE_VAR_NAME = 'GITHUB_EXTENDED_PERMISSIONS'

    GITHUB_ORGANIZATION = getattr(settings, 'GITHUB_ORGANIZATION', None)

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = GITHUB_USER_DATA_URL + '?' + urlencode({
            'access_token': access_token
        })

        try:
            data = simplejson.load(dsa_urlopen(url))
        except ValueError:
            data = None

        # if we have a github organization defined, test that the current users
        # is a member of that organization.
        if data and self.GITHUB_ORGANIZATION:
            member_url = GITHUB_ORGANIZATION_MEMBER_OF_URL.format(
                org=self.GITHUB_ORGANIZATION,
                username=data.get('login')
            ) + '?' + urlencode({
                'access_token': access_token
            })

            try:
                response = dsa_urlopen(member_url)
            except HTTPError:
                data = None
            else:
                # if the user is a member of the organization, response code
                # will be 204, see:
                #   http://developer.github.com/v3/orgs/members/#response-if-requester-is-an-organization-member-and-user-is-a-member
                if not response.code == 204:
                    data = None

        return data

# Backend definition
BACKENDS = {
    'github': GithubAuth,
}

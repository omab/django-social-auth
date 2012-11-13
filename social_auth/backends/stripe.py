"""
Stripe OAuth2 support.

This backend adds support for Stripe OAuth2 service. The settings
STRIPE_APP_ID and STRIPE_API_SECRET must be defined with the values
given by Stripe application registration process.
"""
from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.exceptions import AuthFailed, AuthCanceled


class StripeBackend(OAuthBackend):
    """Stripe OAuth2 authentication backend"""
    name = 'stripe'
    ID_KEY = 'stripe_user_id'
    EXTRA_DATA = [
        ('stripe_publishable_key', 'stripe_publishable_key'),
        ('access_token', 'access_token'),
        ('livemode', 'livemode'),
        ('token_type', 'token_type'),
        ('refresh_token', 'refresh_token'),
        ('stripe_user_id', 'stripe_user_id'),
    ]

    def get_user_details(self, response):
        """Return user details from Stripe account"""
        return {USERNAME: response.get('stripe_user_id'),
                'email': ''}


class StripeAuth(BaseOAuth2):
    """Facebook OAuth2 support"""
    AUTH_BACKEND = StripeBackend
    AUTHORIZATION_URL = 'https://connect.stripe.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://connect.stripe.com/oauth/token'
    SCOPE_VAR_NAME = 'STRIPE_SCOPE'
    SETTINGS_KEY_NAME = 'STRIPE_APP_ID'
    SETTINGS_SECRET_NAME = 'STRIPE_APP_SECRET'
    # Stripe changes the state parameter on some unclear way and doesn't send
    # the redirect_state value if was defined in redirect_uri, they redirect to
    # the URL defined in the app only
    REDIRECT_STATE = False
    STATE_PARAMETER = False

    def process_error(self, data):
        if self.data.get('error'):
            error = self.data.get('error_description') or self.data['error']
            if self.data['error'] == 'access_denied':
                raise AuthCanceled(self, error)
            else:
                raise AuthFailed(self, error)

    def auth_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'response_type': self.RESPONSE_TYPE,
            'client_id': client_id
        }

    def auth_complete_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'scope': self.SCOPE_SEPARATOR.join(self.get_scope()),
            'code': self.data['code']
       }

    def auth_complete_headers(self):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer %s' % client_secret
        }


# Backend definition
BACKENDS = {
    'stripe': StripeAuth
}

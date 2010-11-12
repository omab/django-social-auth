"""Conf settings"""
# Twitter configuration
TWITTER_SERVER                  = 'api.twitter.com'
TWITTER_REQUEST_TOKEN_URL       = 'https://%s/oauth/request_token' % TWITTER_SERVER
TWITTER_ACCESS_TOKEN_URL        = 'https://%s/oauth/access_token' % TWITTER_SERVER
TWITTER_AUTHORIZATION_URL       = 'http://%s/oauth/authorize' % TWITTER_SERVER
TWITTER_CHECK_AUTH              = 'https://twitter.com/account/verify_credentials.json'
TWITTER_UNAUTHORIZED_TOKEN_NAME = 'twitter_unauthorized_token'

# Facebook configuration
FACEBOOK_SERVER            = 'graph.facebook.com'
FACEBOOK_AUTHORIZATION_URL = 'https://%s/oauth/authorize' % FACEBOOK_SERVER
FACEBOOK_ACCESS_TOKEN_URL  = 'https://%s/oauth/access_token' % FACEBOOK_SERVER
FACEBOOK_CHECK_AUTH        = 'https://%s/me' % FACEBOOK_SERVER

# OpenID configuration
OLD_AX_ATTRS = [
    ('http://schema.openid.net/contact/email', 'old_email'),
    ('http://schema.openid.net/namePerson', 'old_fullname'),
    ('http://schema.openid.net/namePerson/friendly', 'old_nickname')
]
AX_SCHEMA_ATTRS = [
    # Request both the full name and first/last components since some
    # providers offer one but not the other.
    ('http://axschema.org/contact/email', 'email'),
    ('http://axschema.org/namePerson', 'fullname'),
    ('http://axschema.org/namePerson/first', 'firstname'),
    ('http://axschema.org/namePerson/last', 'lastname'),
    ('http://axschema.org/namePerson/friendly', 'nickname'),
]
AX_ATTRS          = AX_SCHEMA_ATTRS + OLD_AX_ATTRS
SREG_ATTR         = ['email', 'fullname', 'nickname']
OPENID_ID_FIELD   = 'openid_identifier'
SESSION_NAME      = 'openid'
OPENID_GOOGLE_URL = 'https://www.google.com/accounts/o8/id'
OPENID_YAHOO_URL  = 'http://yahoo.com'

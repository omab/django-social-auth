from django.conf import settings

if getattr(settings,'SOCIAL_AUTH_TEST_TWITTER', True):
    from social_auth.tests.twitter import *
if getattr(settings,'SOCIAL_AUTH_TEST_FACEBOOK', True):
    from social_auth.tests.facebook import *
if getattr(settings,'SOCIAL_AUTH_TEST_GOOGLE', True):
    from social_auth.tests.google import *

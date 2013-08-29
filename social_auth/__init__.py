"""
Django-social-auth application, allows OpenId or OAuth user
registration/authentication just adding a few configurations.
"""
from django.conf import settings


version = (0, 8, 0)
__version__ = '.'.join(map(str, version))


MODELS = getattr(settings, 'SOCIAL_AUTH_MODELS',
                 'social_auth.db.django_models')
IS_DJANGO_MODELS = MODELS == 'social_auth.db.django_models'

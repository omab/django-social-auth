"""Centralized definition of settings"""


from django.utils import importlib
from social_auth.utils import setting


SOCIAL_AUTH_MODELS = setting('SOCIAL_AUTH_MODELS', 'social_auth.django_models')


def get_models_module():
    """Load and return the module specified by the SOCIAL_AUTH_MODELS config
    setting.

    """
    return importlib.import_module(SOCIAL_AUTH_MODELS)

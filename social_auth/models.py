"""Social auth models"""
import types

from django.utils.importlib import import_module

from social_auth.utils import setting


SOCIAL_AUTH_MODELS_MODULE = import_module(setting('SOCIAL_AUTH_MODELS',
                                               'social_auth.db.django_models'))

globals().update((name, value) for name, value in
                    ((name, getattr(SOCIAL_AUTH_MODELS_MODULE, name))
                        for name in dir(SOCIAL_AUTH_MODELS_MODULE))
                    if isinstance(value, (type, types.ClassType)))

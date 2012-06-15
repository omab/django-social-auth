"""Social auth models"""
# TODO define protocol for implementing modules...


from django.conf import settings
from django.utils import importlib


models_module_name = getattr(settings, 'SOCIAL_AUTH_MODELS',
        'social_auth.django_models')
models_module = importlib.import_module(models_module_name)

this_module = globals()
for key in dir(models_module):
    this_module[key] = getattr(models_module, key)

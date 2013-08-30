from django.conf import settings

from social.backends.utils import load_backends, get_backend
from social.backends.open_id import OpenIdAuth as OpenIDBackend


def get_backends(force_load=False):
    return load_backends(getattr(settings, 'AUTHENTICATION_BACKENDS', []),
                         force_load)


# placate pyflakes
OpenIDBackend
get_backend

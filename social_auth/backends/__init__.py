from django.conf import settings
from django.utils.importlib import import_module

from social.backends.base import BaseAuth
from social.backends.open_id import OpenIdAuth as OpenIDBackend


OpenIDBackend  # placate pyflakes

# Cache for discovered backends.
BACKENDSCACHE = {}


def get_backends(force_load=False):
    """
    Entry point to the BACKENDS cache. If BACKENDSCACHE hasn't been
    populated, each of the modules referenced in
    AUTHENTICATION_BACKENDS is imported and checked for a BACKENDS
    definition and if enabled, added to the cache.

    Previously all backends were attempted to be loaded at
    import time of this module, which meant that backends that subclass
    bases found in this module would not have the chance to be loaded
    by the time they were added to this module's BACKENDS dict. See:
    https://github.com/omab/django-social-auth/issues/204

    This new approach ensures that backends are allowed to subclass from
    bases in this module and still be picked up.

    A force_load boolean arg is also provided so that get_backend
    below can retry a requested backend that may not yet be discovered.
    """
    if not BACKENDSCACHE or force_load:
        for auth_backend in getattr(settings, 'AUTHENTICATION_BACKENDS', []):
            mod, cls_name = auth_backend.rsplit('.', 1)
            module = import_module(mod)
            backend = getattr(module, cls_name)

            if issubclass(backend, BaseAuth):
                BACKENDSCACHE[backend.name] = backend
    return BACKENDSCACHE


def get_backend(name, *args, **kwargs):
    """Returns a backend by name. Backends are stored in the BACKENDSCACHE
    cache dict. If not found, each of the modules referenced in
    AUTHENTICATION_BACKENDS is imported and checked for a BACKENDS
    definition. If the named backend is found in the module's BACKENDS
    definition, it's then stored in the cache for future access.
    """
    try:
        # Cached backend which has previously been discovered.
        return BACKENDSCACHE[name](*args, **kwargs)
    except KeyError:
        # Force a reload of BACKENDS to ensure a missing
        # backend hasn't been missed.
        get_backends(force_load=True)
        try:
            return BACKENDSCACHE[name](*args, **kwargs)
        except KeyError:
            return None

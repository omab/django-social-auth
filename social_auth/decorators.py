from functools import wraps

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.utils.importlib import import_module

from social_auth.backends import get_backend
from social_auth.utils import setting, log, backend_setting


LOGIN_ERROR_URL = setting('LOGIN_ERROR_URL', setting('LOGIN_URL'))
PROCESS_EXCEPTIONS = setting('SOCIAL_AUTH_PROCESS_EXCEPTIONS',
                             'social_auth.utils.log_exceptions_to_messages')


def dsa_view(redirect_name=None):
    """Decorate djangos-social-auth views. Will check and retrieve backend
    or return HttpResponseServerError if backend is not found.

        redirect_name parameter is used to build redirect URL used by backend.
    """
    def dec(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            if redirect_name:
                redirect = reverse(redirect_name, args=(backend,))
            else:
                redirect = request.path
            backend = get_backend(backend, request, redirect)

            if not backend:
                return HttpResponseServerError('Incorrect authentication ' +
                                               'service')

            RAISE_EXCEPTIONS = backend_setting(backend,
                                               'SOCIAL_AUTH_RAISE_EXCEPTIONS',
                                               setting('DEBUG'))
            try:
                return func(request, backend, *args, **kwargs)
            except Exception, e:  # some error ocurred
                if RAISE_EXCEPTIONS:
                    raise
                log('error', unicode(e), exc_info=True, extra={
                    'request': request
                })

                url = None
                mod, func_name = PROCESS_EXCEPTIONS.rsplit('.', 1)
                try:
                    process = getattr(import_module(mod), func_name,
                                      lambda *args: None)
                except ImportError:
                    pass
                else:
                    url = process(request, backend, e)

                if not url:
                    url = backend_setting(
                        backend,
                        'SOCIAL_AUTH_BACKEND_ERROR_URL',
                        LOGIN_ERROR_URL
                    )
                return HttpResponseRedirect(url)
        return wrapper
    return dec

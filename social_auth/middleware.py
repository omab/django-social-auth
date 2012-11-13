# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from social_auth.exceptions import SocialAuthBaseException
from social_auth.utils import setting, backend_setting, get_backend_name


class SocialAuthExceptionMiddleware(object):
    """Middleware that handles Social Auth AuthExceptions by providing the user
    with a message, logging an error, and redirecting to some next location.

    By default, the exception message itself is sent to the user and they are
    redirected to the location specified in the LOGIN_ERROR_URL setting.

    This middleware can be extended by overriding the get_message or
    get_redirect_uri methods, which each accept request and exception.
    """
    def process_exception(self, request, exception):
        self.backend = self.get_backend(request, exception)
        if self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            backend_name = get_backend_name(self.backend)
            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)

            if request.user.is_authenticated():
                # Ensure that messages are added to authenticated users only,
                # otherwise this fails
                if backend_name:
                    extra_tags = u'social-auth %s' % backend_name
                else:
                    extra_tags = ''
                messages.error(request, message, extra_tags=extra_tags)
            else:
                url += ('?' in url and '&' or '?') + 'message=' + message
                if backend_name:
                    url += '&backend=' + backend_name
            return redirect(url)

    def get_backend(self, request, exception):
        if not hasattr(self, 'backend'):
            self.backend = getattr(request, 'backend', None) or \
                           getattr(exception, 'backend', None)
        return self.backend

    def raise_exception(self, request, exception):
        backend = self.backend
        return backend and \
               backend_setting(backend, 'SOCIAL_AUTH_RAISE_EXCEPTIONS') or \
               setting('DEBUG')

    def get_message(self, request, exception):
        return unicode(exception)

    def get_redirect_uri(self, request, exception):
        if self.backend is not None:
            return backend_setting(self.backend,
                                   'SOCIAL_AUTH_BACKEND_ERROR_URL',
                                   settings.LOGIN_ERROR_URL)
        return settings.LOGIN_ERROR_URL

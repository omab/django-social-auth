# -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from social_auth.backends.exceptions import AuthException


class SocialAuthExceptionMiddleware(object):
    """Middleware that handles Social Auth AuthExceptions by providing the user
    with a message, logging an error, and redirecting to some next location.

    By default, the exception message itself is sent to the user and they are
    redirected to the location specified in the LOGIN_ERROR_URL setting.

    This middleware can be extended by overriding the get_message or
    get_redirect_uri methods, which each accept request and exception.
    """

    def process_exception(self, request, exception):
        if isinstance(exception, AuthException):
            if hasattr(exception.backend, 'AUTH_BACKEND'):
                backend_name = exception.backend.AUTH_BACKEND.name
            else:
                backend_name = exception.backend.name

            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)

            if request.user.is_authenticated():
                # Ensure that messages are added to authenticated users only,
                # otherwise this fails
                messages.error(
                    request,
                    message,
                    extra_tags=u'social-auth {0}'.format(backend_name)
                )
            else:
                url = url + ('?' in url and '&' or '?') \
                          + 'message={0}&backend={1}'.format(message,
                                                             backend_name)
            return redirect(url)

    def get_message(self, request, exception):
        return unicode(exception)

    def get_redirect_uri(self, request, exception):
        return settings.LOGIN_ERROR_URL

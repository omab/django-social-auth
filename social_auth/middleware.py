# -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import get_callable
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from social_auth.backends.exceptions import AuthAlreadyAssociated


AUTH_EXCEPTION_REDIRECT_URI = (getattr(settings,
        'AUTH_EXCEPTION_REDIRECT_URI', None) or '/')


def default_auth_exception_redirect_uri_func(request, exception):
    return AUTH_EXCEPTION_REDIRECT_URI


def get_auth_exception_redirect_uri_func():
    AUTH_EXCEPTION_REDIRECT_URI_FUNC_NAME = getattr(settings,
            'AUTH_EXCEPTION_REDIRECT_URI_FUNC', None)
    if AUTH_EXCEPTION_REDIRECT_URI_FUNC_NAME:
        func = get_callable(AUTH_EXCEPTION_REDIRECT_URI_FUNC_NAME)
        if callable(func):
            return func
    return default_auth_exception_redirect_uri_func


get_auth_exception_redirect_uri = get_auth_exception_redirect_uri_func()


class SocialAuthExceptionMiddleware(object):
    """Handle specific sub-types of social-auth's AuthException that are
    not related to system or configuration errors, where the user can be
    informed of the situations and, possibly, take corrective action.

    Handling entails providing a message to the user via the Django
    messages framework and then redirecting to either the URI specified
    by the current social backend, or a configured default.

    """
    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            messages.error(request, _('That account is already in use '
                'by another user'))
            url = get_auth_exception_redirect_uri(request, exception)
            return redirect(url)


"""Views"""
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from social_auth.backends import get_backend
from social_auth.utils import sanitize_redirect


def _setting(name, default=''):
    return getattr(settings, name, default)

DEFAULT_REDIRECT = _setting('SOCIAL_AUTH_LOGIN_REDIRECT_URL') or \
                   _setting('LOGIN_REDIRECT_URL')
NEW_USER_REDIRECT = _setting('SOCIAL_AUTH_NEW_USER_REDIRECT_URL')
NEW_ASSOCIATION_REDIRECT = _setting('SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL')
DISCONNECT_REDIRECT_URL = _setting('SOCIAL_AUTH_DISCONNECT_REDIRECT_URL')
LOGIN_ERROR_URL = _setting('LOGIN_ERROR_URL', settings.LOGIN_URL)
COMPLETE_URL_NAME = _setting('SOCIAL_AUTH_COMPLETE_URL_NAME', 'socialauth_complete')
ASSOCIATE_URL_NAME = _setting('SOCIAL_AUTH_ASSOCIATE_URL_NAME',
                              'socialauth_associate_complete')
SOCIAL_AUTH_LAST_LOGIN = _setting('SOCIAL_AUTH_LAST_LOGIN',
                                  'social_auth_last_login_backend')
SESSION_EXPIRATION = _setting('SOCIAL_AUTH_SESSION_EXPIRATION', True)


def auth(request, backend):
    """Start authentication process"""
    return auth_process(request, backend, COMPLETE_URL_NAME)


@csrf_exempt  # If provider uses POST it won't be sending a CSRF token
@transaction.commit_on_success
def complete(request, backend):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return complete_process(request, backend)


def complete_process(request, backend):
    """Authentication complete process"""
    user = auth_complete(request, backend)

    if user and getattr(user, 'is_active', True):
        login(request, user)
        # user.social_user is the used UserSocialAuth instance defined
        # in authenticate process
        social_user = user.social_user

        if SESSION_EXPIRATION :
            # Set session expiration date if present and not disabled by
            # setting. Use last social-auth instance for current provider,
            # users can associate several accounts with a same provider.
            if social_user.expiration_delta():
                request.session.set_expiry(social_user.expiration_delta())

        # store last login backend name in session
        request.session[SOCIAL_AUTH_LAST_LOGIN] = social_user.provider

        # Remove possible redirect URL from session, if this is a new account,
        # send him to the new-users-page if defined.
        url = NEW_USER_REDIRECT if NEW_USER_REDIRECT and \
                                   getattr(user, 'is_new', False) else \
              request.session.pop(REDIRECT_FIELD_NAME, '') or \
              DEFAULT_REDIRECT
    else:
        url = LOGIN_ERROR_URL
    return HttpResponseRedirect(url)


@login_required
def associate(request, backend):
    """Authentication starting process"""
    return auth_process(request, backend, ASSOCIATE_URL_NAME)


@csrf_exempt  # If provider uses POST it won't be sending a CSRF token
@login_required
def associate_complete(request, backend):
    """Authentication complete process"""
    if auth_complete(request, backend):
        url = NEW_ASSOCIATION_REDIRECT if NEW_ASSOCIATION_REDIRECT else \
              request.session.pop(REDIRECT_FIELD_NAME, '') or \
              DEFAULT_REDIRECT
    else:
        url = LOGIN_ERROR_URL

    return HttpResponseRedirect(url)


@login_required
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')
    backend.disconnect(request.user, association_id)
    url = request.REQUEST.get(REDIRECT_FIELD_NAME, '') or \
          DISCONNECT_REDIRECT_URL or \
          DEFAULT_REDIRECT
    return HttpResponseRedirect(url)


def auth_process(request, backend, complete_url_name):
    """Authenticate using social backend"""
    redirect = reverse(complete_url_name, args=(backend,))
    backend = get_backend(backend, request, redirect)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')

    # Save any defined redirect_to value into session
    if REDIRECT_FIELD_NAME in request.REQUEST:
        data = request.POST if request.method == 'POST' else request.GET
        if REDIRECT_FIELD_NAME in data:
            # Check and sanitize a user-defined GET/POST redirect_to field value.
            redirect = sanitize_redirect(request.get_host(),
                                         data[REDIRECT_FIELD_NAME])
            request.session[REDIRECT_FIELD_NAME] = redirect or DEFAULT_REDIRECT

    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')


def auth_complete(request, backend):
    """Complete auth process. Return authenticated user or None."""
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')

    user = request.user if request.user.is_authenticated() else None

    try:
        user = backend.auth_complete(user=user)
    except ValueError, e:  # some Authentication error ocurred
        error_key = getattr(settings, 'SOCIAL_AUTH_ERROR_KEY', None)
        if error_key:  # store error in session
            request.session[error_key] = str(e)
    return user

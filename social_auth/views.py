"""Views

Notes:
    * Some views are marked to avoid csrf tocken check becuase they relay
      on third party providers that (if using POST) won't be sending crfs
      token back.
"""
from functools import wraps

from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from social_auth.backends import get_backend
from social_auth.utils import sanitize_redirect, setting, log


DEFAULT_REDIRECT = setting('SOCIAL_AUTH_LOGIN_REDIRECT_URL') or \
                   setting('LOGIN_REDIRECT_URL')
LOGIN_ERROR_URL = setting('LOGIN_ERROR_URL', setting('LOGIN_URL'))
RAISE_EXCEPTIONS = setting('SOCIAL_AUTH_RAISE_EXCEPTIONS', setting('DEBUG'))


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
                return HttpResponseServerError('Incorrect authentication ' + \
                                               'service')

            try:
                return func(request, backend, *args, **kwargs)
            except Exception, e:  # some error ocurred
                if RAISE_EXCEPTIONS:
                    raise
                backend_name = backend.AUTH_BACKEND.name

                log('error', unicode(e), exc_info=True,
                    extra=dict(request=request))

                if 'django.contrib.messages' in setting('INSTALLED_APPS'):
                    from django.contrib.messages.api import error
                    error(request, unicode(e), extra_tags=backend_name)
                else:
                    log('warn', 'Messages framework not in place, some '+
                                'errors have not been shown to the user.')

                url = setting('SOCIAL_AUTH_BACKEND_ERROR_URL', LOGIN_ERROR_URL)
                return HttpResponseRedirect(url)
        return wrapper
    return dec


@dsa_view(setting('SOCIAL_AUTH_COMPLETE_URL_NAME', 'socialauth_complete'))
def auth(request, backend):
    """Start authentication process"""
    return auth_process(request, backend)


@csrf_exempt
@dsa_view()
def complete(request, backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return complete_process(request, backend, *args, **kwargs)


@login_required
@dsa_view(setting('SOCIAL_AUTH_ASSOCIATE_URL_NAME',
                  'socialauth_associate_complete'))
def associate(request, backend):
    """Authentication starting process"""
    return auth_process(request, backend)


@csrf_exempt
@login_required
@dsa_view()
def associate_complete(request, backend, *args, **kwargs):
    """Authentication complete process"""
    # pop redirect value before the session is trashed on login()
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '')
    user = auth_complete(request, backend, request.user, *args, **kwargs)

    if not user:
        url = LOGIN_ERROR_URL
    elif isinstance(user, HttpResponse):
        return user
    else:
        url = setting('SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL') or \
              redirect_value or \
              DEFAULT_REDIRECT
    return HttpResponseRedirect(url)


@login_required
@dsa_view()
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    backend.disconnect(request.user, association_id)
    url = request.REQUEST.get(REDIRECT_FIELD_NAME, '') or \
          setting('SOCIAL_AUTH_DISCONNECT_REDIRECT_URL') or \
          DEFAULT_REDIRECT
    return HttpResponseRedirect(url)


def auth_process(request, backend):
    """Authenticate using social backend"""
    # Save any defined next value into session
    data = request.POST if request.method == 'POST' else request.GET
    if REDIRECT_FIELD_NAME in data:
        # Check and sanitize a user-defined GET/POST next field value
        redirect = data[REDIRECT_FIELD_NAME]
        if setting('SOCIAL_AUTH_SANITIZE_REDIRECTS', True):
            redirect = sanitize_redirect(request.get_host(), redirect)
        request.session[REDIRECT_FIELD_NAME] = redirect or DEFAULT_REDIRECT

    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')


def complete_process(request, backend, *args, **kwargs):
    """Authentication complete process"""
    # pop redirect value before the session is trashed on login()
    redirect_value = request.session.get(REDIRECT_FIELD_NAME, '')
    user = auth_complete(request, backend, *args, **kwargs)

    if isinstance(user, HttpResponse):
        return user

    if user:
        if getattr(user, 'is_active', True):
            login(request, user)
            # user.social_user is the used UserSocialAuth instance defined
            # in authenticate process
            social_user = user.social_user

            if setting('SOCIAL_AUTH_SESSION_EXPIRATION', True):
                # Set session expiration date if present and not disabled by
                # setting. Use last social-auth instance for current provider,
                # users can associate several accounts with a same provider.
                if social_user.expiration_delta():
                    request.session.set_expiry(social_user.expiration_delta())

            # store last login backend name in session
            key = setting('SOCIAL_AUTH_LAST_LOGIN',
                          'social_auth_last_login_backend')
            request.session[key] = social_user.provider

            # Remove possible redirect URL from session, if this is a new
            # account, send him to the new-users-page if defined.
            new_user_redirect = setting('SOCIAL_AUTH_NEW_USER_REDIRECT_URL')
            if new_user_redirect and getattr(user, 'is_new', False):
                url = new_user_redirect
            else:
                url = redirect_value or DEFAULT_REDIRECT
        else:
            url = setting('SOCIAL_AUTH_INACTIVE_USER_URL', LOGIN_ERROR_URL)
    else:
        msg = setting('LOGIN_ERROR_MESSAGE', None)
        if msg:
            messages.error(request, msg)
        url = LOGIN_ERROR_URL
    return HttpResponseRedirect(url)


def auth_complete(request, backend, user=None, *args, **kwargs):
    """Complete auth process. Return authenticated user or None."""
    if user and not user.is_authenticated():
        user = None

    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    if request.session.get(name):
        data = request.session.pop(name)
        request.session.modified = True
        idx, args, kwargs = backend.from_session_dict(data, user=user,
                                                      request=request,
                                                      *args, **kwargs)
        return backend.continue_pipeline(pipeline_index=idx, *args, **kwargs)
    else:
        return backend.auth_complete(user=user, request=request, *args, **kwargs)

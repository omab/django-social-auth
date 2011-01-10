"""Views"""
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from .auth import get_backend


def auth(request, backend):
    """Start authentication process"""
    complete_url = getattr(settings, 'SOCIAL_AUTH_COMPLETE_URL_NAME',
                           'complete')
    redirect = getattr(settings, 'LOGIN_REDIRECT_URL', '')
    return auth_process(request, backend, complete_url, redirect)


def complete(request, backend):
    """Authentication complete process"""
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')
    user = backend.auth_complete()
    if user and getattr(user, 'is_active', True):
        login(request, user)
        url = request.session.pop(REDIRECT_FIELD_NAME, '') or \
              getattr(settings, 'LOGIN_REDIRECT_URL', '')
    else:
        url = getattr(settings, 'LOGIN_ERROR_URL', settings.LOGIN_URL)
    return HttpResponseRedirect(url)


@login_required
def associate(request, backend):
    """Authentication starting process"""
    complete_url = getattr(settings, 'SOCIAL_AUTH_ASSOCIATE_URL_NAME',
                           'associate_complete')
    redirect = getattr(settings, 'LOGIN_REDIRECT_URL', '')
    return auth_process(request, backend, complete_url, redirect)


@login_required
def associate_complete(request, backend):
    """Authentication complete process"""
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')
    backend.auth_complete(user=request.user)
    url = request.session.pop(REDIRECT_FIELD_NAME, '') or \
          getattr(settings, 'LOGIN_REDIRECT_URL', '')
    return HttpResponseRedirect(url)


def auth_process(request, backend, complete_url_name, default_final_url):
    """Authenticate using social backend"""
    redirect = reverse(complete_url_name, args=(backend,))
    backend = get_backend(backend, request, redirect)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')
    request.session[REDIRECT_FIELD_NAME] = request.GET.get(REDIRECT_FIELD_NAME,
                                                           default_final_url)
    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')

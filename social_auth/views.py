"""Views"""
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib.auth import login, REDIRECT_FIELD_NAME

from .auth import TwitterAuth, FacebookAuth, OpenIdAuth, GoogleAuth, YahooAuth, OrkutAuth


# Authenticatin backends
BACKENDS = {
    'twitter': TwitterAuth,
    'facebook': FacebookAuth,
    'google': GoogleAuth,
    'yahoo': YahooAuth,
    'openid': OpenIdAuth,
    'orkut': OrkutAuth,
}

def auth(request, backend):
    """Authentication starting process"""
    if backend not in BACKENDS:
        return HttpResponseServerError('Incorrect authentication service')
    request.session[REDIRECT_FIELD_NAME] = request.GET.get(REDIRECT_FIELD_NAME,
                                                   settings.LOGIN_REDIRECT_URL)

    redirect = reverse(getattr(settings, 'SOCIAL_AUTH_COMPLETE_URL_NAME',
                               'complete'),
                       args=(backend,))
    backend = BACKENDS[backend](request, redirect)
    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')


def complete(request, backend):
    """Authentication complete process"""
    if backend not in BACKENDS:
        return HttpResponseServerError('Incorrect authentication service')
    backend = BACKENDS[backend](request, request.path)
    user = backend.auth_complete()
    if user and user.is_active:
        login(request, user)
        url = request.session.pop(REDIRECT_FIELD_NAME,
                                  settings.LOGIN_REDIRECT_URL)
    else:
        url = getattr(settings, 'LOGIN_ERROR_URL', settings.LOGIN_URL)
    return HttpResponseRedirect(url)

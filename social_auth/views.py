from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout as auth_logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from .twitter import TwitterOAuth
from .facebook import FacebookOAuth
from .openid_auth import OpenIDAuth, GoogleAuth, YahooAuth


BACKENDS = {
    'twitter': TwitterOAuth,
    'facebook': FacebookOAuth,
    'google': GoogleAuth,
    'yahoo': YahooAuth,
    'openid': OpenIDAuth,
}


def auth(request, backend):
    if backend not in BACKENDS:
        return HttpResponseServerError('Incorrect authentication service')
    request.session[REDIRECT_FIELD_NAME] = request.GET.get(REDIRECT_FIELD_NAME,
                                                           settings.LOGIN_REDIRECT_URL)
    redirect = reverse('social:complete', args=(backend,))
    backend = BACKENDS[backend](request, redirect)
    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')


def complete(request, backend):
    if backend not in BACKENDS:
        return HttpResponseServerError('Incorrect authentication service')
    backend = BACKENDS[backend](request, request.path)
    user = backend.auth_complete()
    if user and user.is_active:
        login(request, user)
    return HttpResponseRedirect(request.session.pop(REDIRECT_FIELD_NAME,
                                                    settings.LOGIN_REDIRECT_URL))


def home(request):
    return HttpResponse(
    """
    <div>
      <h2>OAuth</h2>
      <a href="/login/twitter/">twitter</a>
      <a href="/login/facebook/">facebook</a>
    </div>

    <div>
      <h2>OPenID</h2>
      <a href="/login/google/">google</a>
      <a href="/login/yahoo/">yahoo</a>
      <form action="/login/openid/" method="post">
        provider: <input type="text" value="" name="openid_identifier" />
        <input type="submit" />
      </form>
    </div>
    <br />
    <a href="/logout">logout</a>
    """, content_type='text/html;charset=UTF-8')

@login_required
def done(request):
    user = request.user
    return HttpResponse('%s / %s / %s' % (user.id, user.username, user.first_name))

def logout(request):
    auth_logout(request)
    return HttpResponse('logged out')

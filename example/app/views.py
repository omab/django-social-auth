from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from social_auth import __version__ as version


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('home.html', {'version': version},
                                  RequestContext(request))

@login_required
def done(request):
    """Login complete view, displays user data"""
    names = request.user.social_auth.values_list('provider', flat=True)
    ctx = dict((name.lower().replace('-', '_'), True) for name in names)
    ctx['version'] = version
    return render_to_response('done.html', ctx, RequestContext(request))

def error(request):
    """Error view"""
    return render_to_response('error.html', {'version': version},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

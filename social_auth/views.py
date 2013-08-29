from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from social.actions import do_auth, do_complete, do_disconnect
from social.apps.django_app.utils import strategy
from social.apps.django_app.views import _do_login

from social_auth.utils import load_strategy


@strategy('socialauth_complete', load_strategy=load_strategy)
def auth(request, backend):
    return do_auth(request.strategy, redirect_name=REDIRECT_FIELD_NAME)


@csrf_exempt
@strategy('socialauth_complete', load_strategy=load_strategy)
def complete(request, backend, *args, **kwargs):
    return do_complete(request.strategy, _do_login, request.user,
                       redirect_name=REDIRECT_FIELD_NAME, request=request,
                       *args, **kwargs)


@login_required
@strategy(load_strategy=load_strategy)
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    return do_disconnect(request.strategy, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)

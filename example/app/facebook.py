from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from social_auth.models import UserSocialAuth
from social_auth.views import complete as social_complete
from social_auth.utils import setting
from social_auth.backends.facebook import load_signed_request, FacebookBackend

def is_complete_authentication(request):
    return request.user.is_authenticated() and FacebookBackend.__name__ in request.session.get(BACKEND_SESSION_KEY, '')

def get_access_token(user):
    key = str(user.id)
    access_token = cache.get(key)

    # If cache is empty read the database
    if access_token is None:
        try:
            social_user = user.social_user if hasattr(user, 'social_user') \
                                           else UserSocialAuth.objects.get(user=user.id, provider=FacebookBackend.name)
        except UserSocialAuth.DoesNotExist:
            return None

        if social_user.extra_data:
            access_token = social_user.extra_data.get('access_token')
            expires = social_user.extra_data.get('expires')

            cache.set(key, access_token, int(expires) if expires is not None else 0)

    return access_token

# Facebook decorator to setup environment
def facebook_decorator(func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        # User must me logged via FB backend in order to ensure we talk about the same person
        if not is_complete_authentication(request):
            try:
                user = social_complete(request, FacebookBackend.name)
            except ValueError:
                pass # no matter if failed

        # Not recommended way for FB, but still something we need to be aware of
        if isinstance(user, HttpResponse):
            kwargs.update({'auth_response': user})
        # Need to re-check the completion
        else:
            if is_complete_authentication(request):
                kwargs.update({'access_token': get_access_token(request.user)})
            else:
                request.user = AnonymousUser()

        signed_request = load_signed_request(request.REQUEST.get('signed_request', ''))
        if signed_request:
            kwargs.update({'signed_request': signed_request})

        return func(request, *args, **kwargs)

    return wrapper


@csrf_exempt
@facebook_decorator
def facebook_view(request, *args, **kwargs):
    # If there is a ready response just return it. Not recommended though.
    auth_response =  kwargs.get('auth_response')
    if auth_response:
        return auth_response

    return render_to_response('facebook.html', {'fb_app_id':setting('FACEBOOK_APP_ID'),
                                                'warning': request.method == 'GET'}, RequestContext(request))
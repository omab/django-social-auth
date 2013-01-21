from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.core.cache import cache
from django.conf import settings

from social_auth.models import UserSocialAuth
from social_auth.views import complete as social_complete
from social_auth.utils import setting
from social_auth.backends.contrib.vkontakte import VKontakteOAuth2Backend, vkontakte_api

def is_complete_authentication(request):
    return request.user.is_authenticated() and VKontakteOAuth2Backend.__name__ in request.session.get(BACKEND_SESSION_KEY, '')

def get_access_token(user):
    key = str(user.id)
    access_token = cache.get(key)

    # If cache is empty read the database
    if access_token is None:
        try:
            social_user = user.social_user if hasattr(user, 'social_user') \
                                           else UserSocialAuth.objects.get(user=user.id, provider=VKontakteOAuth2Backend.name)
        except UserSocialAuth.DoesNotExist:
            return None

        if social_user.extra_data:
            access_token = social_user.extra_data.get('access_token')
            expires = social_user.extra_data.get('expires')

            cache.set(key, access_token, int(expires) if expires is not None else 0)

    return access_token

# VK decorator to setup environment
def vkontakte_decorator(func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        # User must me logged via VKontakte backend in order to ensure we talk about the same person
        if not is_complete_authentication(request):
            try:
                user = social_complete(request, VKontakteOAuth2Backend.name)
            except (ValueError, AttributeError):
                pass # no matter if failed

        # Not recommended way for VK, but still something we need to be aware of
        if isinstance(user, HttpResponse):
            kwargs.update({'auth_response': user})
        # Need to re-check the completion
        else:
            if is_complete_authentication(request):
                kwargs.update({'access_token': get_access_token(request.user)})
            else:
                request.user = AnonymousUser()

        return func(request, *args, **kwargs)

    return wrapper

@vkontakte_decorator
def vkontakte_view(request, *args, **kwargs):
    # If there is a ready response just return it. Not recommended because pipeline redirects fail the normal workflow
    # here.
    auth_response = kwargs.get('auth_response')
    if auth_response:
        for item in auth_response.items():
            if item[0] == 'Location' and 'form' in item[1]:
                return auth_response

    return render_to_response('vkontakte_app.html',
                                {'vk_app_id': settings.VKONTAKTE_APP_AUTH['id'] if hasattr(settings, 'VKONTAKTE_APP_AUTH') else None,
                                 'app_scope': ','.join(settings.VKONTAKTE_OAUTH2_EXTRA_SCOPE),
                                 'warning': not request.GET.get('user_id')},
                                RequestContext(request))
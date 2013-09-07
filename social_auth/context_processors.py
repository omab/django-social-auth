from collections import defaultdict

from social.apps.django_app.context_processors import login_redirect, \
                                                      backends, LazyDict
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.open_id import OpenIdAuth
from social.utils import user_is_authenticated

from social_auth.models import UserSocialAuth
from social_auth.backends import get_backends

# Note: social_auth_backends, social_auth_by_type_backends and
#       social_auth_by_name_backends don't play nice together.


def social_auth_backends(request):
    """Load Social Auth current user data to context.
    Will add a output from backends_data to context under social_auth key.
    """
    return {'social_auth': backends(request)}


def social_auth_by_type_backends(request):
    """Load Social Auth current user data to context.
    Will add a output from backends_data to context under social_auth key where
    each entry will be grouped by backend type (openid, oauth, oauth2).
    """
    def context_value():
        data = dict(backends(request)['backends'])
        data['backends'] = group_backend_by_type(data['backends'])
        data['not_associated'] = group_backend_by_type(data['not_associated'])
        data['associated'] = group_backend_by_type(data['associated'])
        return data
    return {'social_auth': LazyDict(context_value)}


def social_auth_by_name_backends(request):
    """Load Social Auth current user data to context.
    Will add a social_auth object whose attribute names are the names of each
    provider, e.g. social_auth.facebook would be the facebook association or
    None, depending on the logged in user's current associations. Providers
    with a hyphen have the hyphen replaced with an underscore, e.g.
    google-oauth2 becomes google_oauth2 when referenced in templates.
    """
    def context_value():
        keys = [key for key in get_backends().keys()]
        accounts = dict(zip(keys, [None] * len(keys)))
        user = request.user
        if user_is_authenticated(user):
            accounts.update((assoc.provider, assoc)
                    for assoc in UserSocialAuth.get_social_auth_for_user(user))
        return accounts
    return {'social_auth': LazyDict(context_value)}


def social_auth_login_redirect(request):
    """Load current redirect to context."""
    data = login_redirect(request)
    data['redirect_querystring'] = data.get('REDIRECT_QUERYSTRING')
    return data


def group_backend_by_type(items):
    """Group items by backend type."""
    result = defaultdict(list)
    backends_defined = get_backends()

    for item in items:
        name = getattr(item, 'provider', item)
        backend = backends_defined[name]
        if issubclass(backend, OpenIdAuth):
            result['openid'].append(item)
        elif issubclass(backend, BaseOAuth2):
            result['oauth2'].append(item)
        elif issubclass(backend, BaseOAuth1):
            result['oauth'].append(item)
    return dict(result)

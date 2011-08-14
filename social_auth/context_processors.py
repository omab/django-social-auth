from social_auth.backends import BACKENDS
from social_auth.utils import group_backend_by_type


# Note: social_auth_backends and social_auth_by_type_backends don't play nice
#       together

def social_auth_backends(request):
    """Load Social Auth current user data to context.
    Will add a output from backends_data to context under social_auth key.
    """
    return {'social_auth': backends_data(request.user)}


def social_auth_by_type_backends(request):
    """Load Social Auth current user data to context.
    Will add a output from backends_data to context under social_auth key where
    each entry will be grouped by backend type (openid, oauth, oauth2).
    """
    data = backends_data(request.user)
    data['backends'] = group_backend_by_type(data['backends'])
    data['not_associated'] = group_backend_by_type(data['not_associated'])
    data['associated'] = group_backend_by_type(data['associated'],
                                               key=lambda assoc: assoc.provider)
    return {'social_auth': data}


def backends_data(user):
    """Return backends data for given user.

    Will return a dict with values:
        associated: UserSocialAuth model instances for currently
                    associated accounts
        not_associated: Not associated (yet) backend names.
        backends: All backend names.

    If user is not authenticated, then first list is empty, and there's no
    difference between the second and third lists.
    """
    available = BACKENDS.keys()
    values = {'associated': [],
              'not_associated': available,
              'backends': available}

    if user.is_authenticated():
        associated = user.social_auth.all()
        not_associated = list(set(available) -
                              set(assoc.provider for assoc in associated))
        values['associated'] = associated
        values['not_associated'] = not_associated
    return values

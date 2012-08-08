from uuid import uuid4

from social_auth.utils import setting
from social_auth.models import UserSocialAuth
from social_auth.backends import USERNAME
from social_auth.signals import socialauth_registered, \
                                pre_update


def get_username(details, user=None,
                 user_exists=UserSocialAuth.simple_user_exists,
                 *args, **kwargs):
    """Return an username for new user. Return current user username
    if user was given.
    """
    if user:
        return {'username': user.username}

    if details.get(USERNAME):
        username = unicode(details[USERNAME])
    else:
        username = uuid4().get_hex()

    uuid_length = 16
    max_length = UserSocialAuth.username_max_length()
    short_username = username[:max_length - uuid_length]
    final_username = username[:max_length]

    # Generate a unique username for current user using username
    # as base but adding a unique hash at the end. Original
    # username is cut to avoid any field max_length.
    while user_exists(username=final_username):
        username = short_username + uuid4().get_hex()[:uuid_length]
        final_username = username[:max_length]

    return {'username': final_username}


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None
    # NOTE: not return None because Django raises exception of strip email
    email = details.get('email') or ''
    return {
        'user': UserSocialAuth.create_user(username=username, email=email),
        'is_new': True
    }


def update_user_details(backend, details, response, user, is_new=False, *args,
                        **kwargs):
    """Update user details using data from provider."""
    changed = False  # flag to track changes

    for name, value in details.iteritems():
        # do not update username, it was already generated
        # do not update configured fields if user already existed
        if name in (USERNAME, 'id', 'pk') or (not is_new and
            name in setting('SOCIAL_AUTH_PROTECTED_USER_FIELDS', [])):
            continue
        if value and value != getattr(user, name, None):
            setattr(user, name, value)
            changed = True

    # Fire a pre-update signal sending current backend instance,
    # user instance (created or retrieved from database), service
    # response and processed details.
    #
    # Also fire socialauth_registered signal for newly registered
    # users.
    #
    # Signal handlers must return True or False to signal instance
    # changes. Send method returns a list of tuples with receiver
    # and it's response.
    signal_response = lambda (receiver, response): response
    signal_kwargs = {'sender': backend.__class__, 'user': user,
                     'response': response, 'details': details}

    changed |= any(filter(signal_response, pre_update.send(**signal_kwargs)))

    # Fire socialauth_registered signal on new user registration
    if is_new:
        changed |= any(filter(signal_response,
                              socialauth_registered.send(**signal_kwargs)))

    if changed:
        user.save()

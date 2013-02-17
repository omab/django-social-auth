from uuid import uuid4

from django.template.defaultfilters import slugify

from social_auth.utils import setting
from social_auth.models import UserSocialAuth


def get_username(details, user=None,
                 user_exists=UserSocialAuth.simple_user_exists,
                 *args, **kwargs):
    """Return an username for new user. Return current user username
    if user was given.
    """
    if user:
        return {'username': user.username}

    email_as_username = setting('SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL', False)
    uuid_length = setting('SOCIAL_AUTH_UUID_LENGTH', 16)
    do_slugify = setting('SOCIAL_AUTH_SLUGIFY_USERNAMES', False)

    if email_as_username and details.get('email'):
        username = details['email']
    elif details.get('username'):
        username = unicode(details['username'])
    else:
        username = uuid4().get_hex()

    max_length = UserSocialAuth.username_max_length()
    short_username = username[:max_length - uuid_length]
    final_username = UserSocialAuth.clean_username(username[:max_length])
    if do_slugify:
        final_username = slugify(final_username)

    # Generate a unique username for current user using username
    # as base but adding a unique hash at the end. Original
    # username is cut to avoid any field max_length.
    while user_exists(username=final_username):
        username = short_username + uuid4().get_hex()[:uuid_length]
        username = username[:max_length]
        final_username = UserSocialAuth.clean_username(username)
        if do_slugify:
            final_username = slugify(final_username)
    return {'username': final_username}


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None

    # Avoid hitting field max length
    email = details.get('email')
    original_email = None
    if email and UserSocialAuth.email_max_length() < len(email):
        original_email = email
        email = ''

    return {
        'user': UserSocialAuth.create_user(username=username,
                                           email=email),
        'original_email': original_email,
        'is_new': True
    }


def update_user_details(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    """Update user details using data from provider."""
    if user is None:
        return

    changed = False  # flag to track changes

    for name, value in details.iteritems():
        # do not update username, it was already generated
        # do not update configured fields if user already existed
        if name in ('username', 'id', 'pk') or (not is_new and
           name in setting('SOCIAL_AUTH_PROTECTED_USER_FIELDS', [])):
            continue
        if value and value != getattr(user, name, None):
            setattr(user, name, value)
            changed = True

    if changed:
        user.save()

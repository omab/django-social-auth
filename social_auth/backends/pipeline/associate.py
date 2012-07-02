from social_auth.utils import setting
from social_auth.models import get_user_by_email
from social_auth.backends.pipeline import warn_setting
from social_auth.backends.exceptions import AuthException


def associate_by_email(details, *args, **kwargs):
    """Return user entry with same email address as one returned on details."""
    email = details.get('email')

    warn_setting('SOCIAL_AUTH_ASSOCIATE_BY_MAIL', 'associate_by_email')

    if email and setting('SOCIAL_AUTH_ASSOCIATE_BY_MAIL', True):
        # try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned
        try:
            return {'user': get_user_by_email(email=email)}
        except User.MultipleObjectsReturned:
            raise AuthException(kwargs['backend'], 'Not unique email address.')
        except User.DoesNotExist:
            pass

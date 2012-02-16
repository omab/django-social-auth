from django.core.exceptions import MultipleObjectsReturned

from social_auth.utils import setting
from social_auth.models import User
from social_auth.backends.pipeline import warn_setting


def associate_by_email(details, *args, **kwargs):
    """Return user entry with same email address as one returned on details."""
    email = details.get('email')

    warn_setting('SOCIAL_AUTH_ASSOCIATE_BY_MAIL', 'associate_by_email')

    if email and setting('SOCIAL_AUTH_ASSOCIATE_BY_MAIL'):
        # try to associate accounts registered with the same email address,
        # only if it's a single object. ValueError is raised if multiple
        # objects are returned
        try:
            return {'user': User.objects.get(email=email)}
        except MultipleObjectsReturned:
            raise ValueError('Not unique email address.')
        except User.DoesNotExist:
            pass

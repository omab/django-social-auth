"""Django-Social-Auth Pipeline.

Pipelines must return a dictionary with values that will be passed as parameter
to next pipeline item. Pipelines must take **kwargs parameters to avoid
failure. At some point a pipeline entry must create a UserSocialAuth instance
and load it to the output if the user logged in correctly.
"""
import warnings

from django.conf import settings

from social_auth.models import User


USERNAME = 'username'
USERNAME_MAX_LENGTH = User._meta.get_field(USERNAME).max_length


def warn_setting(name, func_name):
    """Warn about deprecated settings."""
    if hasattr(settings, name):
        msg = '%s is deprecated, disable or override "%s" pipeline instead'
        warnings.warn(msg % (name, func_name))

"""Django ORM models for Social Auth"""
from datetime import timedelta

from django.db import models

from social_auth.fields import JSONField
from social_auth.utils import setting


NAME = 'django_models'


# If User class is overridden, it *must* provide the following fields
# and methods work with django-social-auth:
#
#   username   = CharField()
#   last_login = DateTimeField()
#   is_active  = BooleanField()
#   def is_authenticated():
#       ...

if setting('SOCIAL_AUTH_USER_MODEL'):
    User = models.get_model(*setting('SOCIAL_AUTH_USER_MODEL').rsplit('.', 1))
else:
    from django.contrib.auth.models import User


# TODO make this a complementary config setting to SOCIAL_AUTH_USER_MODEL
USERNAME = 'username'
USERNAME_MAX_LENGTH = User._meta.get_field(USERNAME).max_length


def simple_user_exists(*args, **kwargs):
    """Return True/False if a User instance exists with the given arguments.
    Arguments are directly passed to filter() manager method."""
    return User.objects.filter(*args, **kwargs).exists()


def create_user(*args, **kwargs):
    return User.objects.create_user(*args, **kwargs)


def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def get_user_by_email(email):
    return User.objects.get(email=email)


def get_social_auth_for_user(user):
    return user.social_auth.all()


class UserSocialAuth(models.Model):
    """Social Auth association model"""
    user = models.ForeignKey(User, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = JSONField(default='{}')

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        app_label = 'social_auth'

    def __unicode__(self):
        """Return associated user unicode representation"""
        return u'%s - %s' % (unicode(self.user), self.provider.title())

    @property
    def tokens(self):
        """Return access_token stored in extra_data or None"""
        # Make import here to avoid recursive imports :-/
        from social_auth.backends import get_backends
        backend = get_backends().get(self.provider)
        if backend:
            return backend.AUTH_BACKEND.tokens(self)
        else:
            return {}

    def expiration_delta(self):
        """Return saved session expiration seconds if any. Is returned in
        the form of a timedelta data type. None is returned if there's no
        value stored or it's malformed.
        """
        if self.extra_data:
            name = setting('SOCIAL_AUTH_EXPIRATION', 'expires')
            try:
                return timedelta(seconds=int(self.extra_data.get(name)))
            except (ValueError, TypeError):
                pass
        return None

    @classmethod
    def select_related(cls):
        return cls.objects.select_related('user')


class Nonce(models.Model):
    """One use numbers"""
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        app_label = 'social_auth'

    def __unicode__(self):
        """Unicode representation"""
        return self.server_url


class Association(models.Model):
    """OpenId account association"""
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        app_label = 'social_auth'

    def __unicode__(self):
        """Unicode representation"""
        return '%s %s' % (self.handle, self.issued)

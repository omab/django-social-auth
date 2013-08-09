"""Django ORM models for Social Auth"""
from django.db import models
from django.db.models.loading import get_model
from django.db.utils import IntegrityError

from social_auth.db.base import UserSocialAuthMixin, AssociationMixin, \
                                NonceMixin
from social_auth.fields import JSONField
from social_auth.utils import setting


# If User class is overridden, it *must* provide the following fields
# and methods work with django-social-auth:
#
#   username   = CharField()
#   last_login = DateTimeField()
#   is_active  = BooleanField()
#   def is_authenticated():
#       ...
USER_MODEL = setting('SOCIAL_AUTH_USER_MODEL') or \
             setting('AUTH_USER_MODEL') or \
             'auth.User'
UID_LENGTH = setting('SOCIAL_AUTH_UID_LENGTH', 255)
NONCE_SERVER_URL_LENGTH = setting('SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH', 255)
ASSOCIATION_SERVER_URL_LENGTH = setting(
    'SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH',
    255
)
ASSOCIATION_HANDLE_LENGTH = setting(
    'SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH',
    255
)


class UserSocialAuth(models.Model, UserSocialAuthMixin):
    """Social Auth association model"""
    user = models.ForeignKey(USER_MODEL, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    extra_data = JSONField(default='{}')

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        app_label = 'social_auth'

    @classmethod
    def get_social_auth(cls, provider, uid):
        try:
            return cls.objects.select_related('user').get(provider=provider,
                                                          uid=uid)
        except UserSocialAuth.DoesNotExist:
            return None

    @classmethod
    def username_max_length(cls):
        return cls._field_length('USERNAME_FIELD', 'username')

    @classmethod
    def email_max_length(cls):
        return cls._field_length('EMAIL_FIELD', 'email')

    @classmethod
    def _field_length(self, setting_name, default_name):
        model = UserSocialAuth.user_model()
        field_name = getattr(model, setting_name, default_name)
        return model._meta.get_field(field_name).max_length

    @classmethod
    def user_model(cls):
        return get_model(*USER_MODEL.split('.'))


class Nonce(models.Model, NonceMixin):
    """One use numbers"""
    server_url = models.CharField(max_length=NONCE_SERVER_URL_LENGTH)
    timestamp = models.IntegerField(db_index=True)
    salt = models.CharField(max_length=40)

    class Meta:
        app_label = 'social_auth'
        unique_together = ('server_url', 'timestamp', 'salt')


class Association(models.Model, AssociationMixin):
    """OpenId account association"""
    server_url = models.CharField(max_length=ASSOCIATION_SERVER_URL_LENGTH)
    handle = models.CharField(max_length=ASSOCIATION_HANDLE_LENGTH)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField(db_index=True)
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        app_label = 'social_auth'
        unique_together = ('server_url', 'handle')


def is_integrity_error(exc):
    return exc.__class__ is IntegrityError

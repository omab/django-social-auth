"""Django ORM models for Social Auth"""


import base64
from datetime import timedelta

from django.db import models
from openid.association import Association as OIDAssociation

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


def resolve_user_or_id(user_or_id):
    if isinstance(user_or_id, User):
       return user_or_id
    return User.objects.get(pk=user_or_id)


def get_social_auth(provider, uid):
    try:
        return UserSocialAuth.objects.select_related('user').get(
                provider=provider, uid=uid)
    except UserSocialAuth.DoesNotExist:
        return None


def get_social_auth_for_user(user):
    return user.social_auth.all()


def create_social_auth(user, uid, provider):
    return UserSocialAuth.objects.create(user=user, uid=uid, provider=provider)


def store_association(server_url, association):
    args = {'server_url': server_url, 'handle': association.handle}
    try:
        assoc = Association.objects.get(**args)
    except Association.DoesNotExist:
        assoc = Association(**args)
    assoc.secret = base64.encodestring(association.secret)
    assoc.issued = association.issued
    assoc.lifetime = association.lifetime
    assoc.assoc_type = association.assoc_type
    assoc.save()


def get_oid_associations(server_url, handle=None):
    args = {'server_url': server_url}
    if handle is not None:
        args['handle'] = handle

    return sorted([
            (assoc.id,
             OIDAssociation(assoc.handle,
                            base64.decodestring(assoc.secret),
                            assoc.issued,
                            assoc.lifetime,
                            assoc.assoc_type))
            for assoc in Association.objects.filter(**args)
    ], key=lambda x: x[1].issued, reverse=True)


def delete_associations(ids_to_delete):
    Association.objects.filter(pk__in=ids_to_delete).delete()


def use_nonce(server_url, timestamp, salt):
    return Nonce.objects.get_or_create(server_url=server_url,
                                       timestamp=timestamp,
                                       salt=salt)[1]


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

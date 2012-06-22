"""MongoEngine models for Social Auth

Requires MongoEngine 0.6.10

"""
# TODO extract common code into base objects/mixins


from datetime import timedelta
from mongoengine import DictField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import ReferenceField
from mongoengine import StringField
from social_auth.utils import setting


NAME = 'mongoengine_models'


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
    from mongoengine.django.auth import User


# TODO make this a complementary config setting to SOCIAL_AUTH_USER_MODEL
USERNAME = 'username'


def get_username_max_length():
    """Get the max length constraint from the User model username field.
    """
    return getattr(User, USERNAME).max_length


def simple_user_exists(*args, **kwargs):
    """Return True/False if a User instance exists with the given arguments.
    Arguments are directly passed to filter() manager method."""
    return User.objects.filter(*args, **kwargs).count()


def create_user(*args, **kwargs):
    return User.objects.create(*args, **kwargs)


def get_social_auth_for_user(user):
    return UserSocialAuth.objects(user=user)


class UserSocialAuth(Document):
    """Social Auth association model"""
    user = ReferenceField(User)
    provider = StringField(max_length=32)
    uid = StringField(max_length=255, unique_with='provider')
    extra_data = DictField()

    def __unicode__(self):
        """Return associated user unicode representation"""
        return u'%s - %s' % (unicode(self.user), self.provider)

    @classmethod
    def select_related(cls):
        return cls.objects #.select_related() No 'user', only provie a depth parameter

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


class Nonce(Document):
    """One use numbers"""
    server_url = StringField(max_length=255)
    timestamp = IntField()
    salt = StringField(max_length=40)

    def __unicode__(self):
        """Unicode representation"""
        return self.server_url


class Association(Document):
    """OpenId account association"""
    server_url = StringField(max_length=255)
    handle = StringField(max_length=255)
    secret = StringField(max_length=255)  # Stored base64 encoded
    issued = IntField()
    lifetime = IntField()
    assoc_type = StringField(max_length=64)

    def __unicode__(self):
        """Unicode representation"""
        return '%s %s' % (self.handle, self.issued)

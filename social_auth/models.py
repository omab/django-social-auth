"""Social auth models"""
from django.db import models 
from django.conf import settings

# If User class is overrided, it must provide the following fields:
#
#   username = CharField()
#   email = EmailField()
#   password = CharField()
#   is_active  = BooleanField()
#
# and methods:
#
#   def is_authenticated():
#       ...
MANDATORY_FIELDS = ('username', 'email', 'password', 'last_login')
MANDATORY_METHODS = ('is_authenticated',)

try: # try to import User model override and validate needed fields
    User = models.get_model(*settings.SOCIAL_AUTH_USER_MODEL.split('.'))
    if not all(User._meta.get_field(name) for name in MANDATORY_FIELDS):
        raise AttributeError, 'Some mandatory field missing'
    if not all(callable(getattr(User, name, None))
                    for name in MANDATORY_METHODS):
        raise AttributeError, 'Some mandatory methods missing'
except AttributeError: # fail silently on missing setting
    from django.contrib.auth.models import User


class UserSocialAuth(models.Model):
    """Social Auth association model"""
    user = models.ForeignKey(User, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.TextField()
    extra_data = models.TextField(default='', blank=True)

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')


class Nonce(models.Model):
    """One use numbers"""
    server_url = models.TextField()
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)


class Association(models.Model):
    """OpenId account association"""
    server_url = models.TextField()
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255) # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

"""Social auth models"""
from django.db import models 
from django.conf import settings

def get_user_model():
    """Allow setting a custom (extended) user model"""
    return models.get_model(*getattr(settings, 'SOCIAL_AUTH_USER_MODEL', 'auth.User').split('.'))

User = get_user_model()

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

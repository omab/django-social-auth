from django.db import models 
from django.contrib.auth.models import User


class UserSocialAuth(models.Model):
    user = models.ForeignKey(User)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=2048)

    class Meta:
        unique_together = ('provider', 'uid')


class Nonce(models.Model):
    server_url = models.CharField(max_length=2047)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)


class Association(models.Model):
    server_url = models.TextField(max_length=2047)
    handle = models.CharField(max_length=255)
    secret = models.TextField(max_length=255) # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField(max_length=64)

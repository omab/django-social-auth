# Define a custom User class to work with django-social-auth
from django.db import models


class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
    username = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    def is_authenticated(self):
        return True


from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend

def facebook_extra_values(sender, user, response, details, **kwargs):
    return False

pre_update.connect(facebook_extra_values, sender=FacebookBackend)

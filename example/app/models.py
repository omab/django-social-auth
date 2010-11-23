# Define a custom User class to work with django-social-auth
#
# from django.db import models
# 
# class CustomUser(models.Model):
#     username = models.CharField(max_length=128)
#     email = models.EmailField()
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     first_name = models.CharField(max_length=128, blank=True)
#     last_name = models.CharField(max_length=128, blank=True)
#     is_active = models.BooleanField(default=True)
# 
#     def is_authenticated(self):
#         return True

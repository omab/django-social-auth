"""Some base classes"""
import os
import md5

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import UNUSABLE_PASSWORD

from .models import UserSocialAuth

# get User class, could not be auth.User
User = UserSocialAuth._meta.get_field('user').rel.to


class BaseAuth(object):
    """Base authentication class, new authenticators should subclass
    and implement needed methods"""
    def __init__(self, request, redirect):
        self.request = request
        self.redirect = redirect

    def auth_url(self):
        """Must return redirect URL to auth provider"""
        raise NotImplementedError, 'Implement in subclass'
    
    def auth_html(self):
        """Must return login HTML content returned by provider"""
        raise NotImplementedError, 'Implement in subclass'
    
    def auth_complete(self):
        """Completes loging process, must return user instance"""
        raise NotImplementedError, 'Implement in subclass'

    @property
    def uses_redirect(self):
        """Return True if this provider uses redirect url method,
        otherwise return false."""
        return True


class SocialAuthBackend(ModelBackend):
    """A django.contrib.auth backend that authenticates the user based on
    a authentication provider response"""
    name = '' # provider name, it's stored in database

    def authenticate(self, **kwargs):
        """Authenticate user using social credentials

        Authentication is made if this is the correct backend, backend
        verification is made by kwargs inspection for current backend
        name presence.
        """

        # Validate backend and arguments. Require that the OAuth response
        # be passed in as a keyword argument, to make sure we don't match
        # the username/password calling conventions of authenticate.
        if not (self.name and kwargs.get(self.name) and 'response' in kwargs):
            return None

        response = kwargs.get('response')
        details = self.get_user_details(response)
        uid = self.get_user_id(details, response)
        try:
            auth_user = UserSocialAuth.objects.select_related('user')\
                                              .get(provider=self.name,
                                                   uid=uid)
        except UserSocialAuth.DoesNotExist:
            if not getattr(settings, 'SOCIAL_AUTH_CREATE_USERS', False):
                return None
            user = self.create_user(response, details)
        else:
            user = auth_user.user
            self.update_user_details(user, details)
        return user
    
    def get_username(self, details):
        """Return an unique username, if SOCIAL_AUTH_FORCE_RANDOM_USERNAME
        setting is True, then username will be a random 30 chars md5 hash
        """
        def get_random_username():
            """Return hash from random string cut at 30 chars"""
            return md5.md5(str(os.urandom(10))).hexdigest()[:30]

        if getattr(settings, 'SOCIAL_AUTH_FORCE_RANDOM_USERNAME', False):
            username = get_random_username()
        elif 'username' in details:
            username = details['username']
        elif hasattr(settings, 'SOCIAL_AUTH_DEFAULT_USERNAME'):
            username = settings.SOCIAL_AUTH_DEFAULT_USERNAME
            if callable(username):
                username = username()
        else:
            username = get_random_username()

        name, idx = username, 2
        while True:
            try:
                User.objects.get(username=name)
                name = username + str(idx)
                idx += 1
            except User.DoesNotExist:
                username = name
                break
        return username

    def create_user(self, response, details):
        """Create user with unique username"""
        username = self.get_username(details)
        email = details.get('email', '')

        if hasattr(User.objects, 'create_user'): # auth.User
            user = User.objects.create_user(username, email)
        else: # create user setting password to an unusable value
            user = User.objects.create(username=username, email=email,
                                       password=UNUSABLE_PASSWORD)

        self.update_user_details(user, details) # load details
        self.associate_auth(user, response, details) # save account association
        return user

    def associate_auth(self, user, response, details):
        """Associate an OAuth with a user account."""
        # Check to see if this OAuth has already been claimed.
        uid = self.get_user_id(details, response)
        try:
            user_oauth = UserSocialAuth.objects.select_related('user')\
                                               .get(provider=self.name,
                                                    uid=uid)
        except UserSocialAuth.DoesNotExist:
            if getattr(settings, 'SOCIAL_AUTH_EXTRA_DATA', True):
                extra_data = self.extra_data(user, uid, response, details)
            else:
                extra_data = ''
            user_oauth = UserSocialAuth.objects.create(user=user, uid=uid,
                                                       provider=self.name,
                                                       extra_data=extra_data)
        else:
            if user_oauth.user != user:
                raise ValueError, 'Identity already claimed'
        return user_oauth

    def extra_data(self, user, uid, response, details):
        """Return default blank user extra data"""
        return ''

    def update_user_details(self, user, details):
        """Update user details with new (maybe) data"""
        fields = user._meta.get_all_field_names()
        changed = False

        for name in ('first_name', 'last_name', 'email'):
            value = details.get(name)
            if name in fields and value != getattr(user, name, value):
                setattr(user, name, value)
                changed = True

        if changed:
            user.save()

    def get_user_id(self, details, response):
        """Must return a unique ID from values returned on details"""
        raise NotImplementedError, 'Implement in subclass'

    def get_user_details(self, response):
        """Must return user details in a know internal struct:
            {'email': <user email if any>,
             'username': <username if any>,
             'fullname': <user full name if any>,
             'first_name': <user first name if any>,
             'last_name': <user last name if any>}
        """
        raise NotImplementedError, 'Implement in subclass'

    def get_user(self, user_id):
        """Return user instance for @user_id"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

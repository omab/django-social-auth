Signals
=======
A ``pre_update`` signal is sent when user data is about to be updated with new
values from authorization service provider, this apply to new users and already
existent ones. This is useful to update custom user fields or `User Profiles`_,
for example, to store user gender, location, etc. Example::

    from social_auth.signals import pre_update
    from social_auth.backends.facebook import FacebookBackend

    def facebook_extra_values(sender, user, response, details, **kwargs):
        user.gender = response.get('gender')
        return True

    pre_update.connect(facebook_extra_values, sender=FacebookBackend)

New data updating is made automatically but could be disabled and left only to
signal handler if this setting value is set to True::

    SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = False

Take into account that when defining a custom ``User`` model and declaring signal
handler in ``models.py``, the imports and handler definition **must** be made
after the custom ``User`` model is defined or circular imports issues will be
raised.

Also a new-user signal (``socialauth_registered``) is sent when new accounts are
created::

    from social_auth.signals import socialauth_registered

    def new_users_handler(sender, user, response, details, **kwargs):
        user.is_new = True
        return False

    socialauth_registered.connect(new_users_handler, sender=None)


.. _User Profiles: http://www.djangobook.com/en/1.0/chapter12/#cn222

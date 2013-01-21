Mixcloud OAuth2
===============

The `Mixcloud API`_ offers support for authorization.
To enable OAuth2 support:

- Register a new application at `Mixcloud Developers`_

- Add Mixcloud backend to ``AUTHENTICATION_BACKENDS`` in settings::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_auth.backends.contrib.mixcloud.MixcloudBackend',
    )

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

    MIXCLOUD_CLIENT_ID = ''
    MIXCLOUD_CLIENT_SECRET = ''

- Similar to the other OAuth backends you can define::

    MIXCLOUD_EXTRA_DATA = [('username', 'username'), ('name', 'name'), ('pictures', 'pictures'), ('url', 'url')]

as a list of tuples ``(response name, alias)`` to store user profile data on the UserSocialAuth model.


.. _Mixcloud API: http://www.mixcloud.com/developers/documentation
.. _Mixcloud Developers: http://www.mixcloud.com/developers

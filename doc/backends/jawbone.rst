Jawbone
=========
Jawbone uses OAuth v2 for Authentication

- Register a new application at the `Jawbone UP Platform`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      JAWBONE_CLIENT_ID = ''
      JAWBONE_CLIENT_SECRET = ''

- extra scopes can be defined by using::

    JAWBONE_EXTENDED_PERMISSIONS = ['basic_read', 'mood_read', 'mood_write']

.. _Jawbone UP Platform: https://jawbone.com/up/platform/

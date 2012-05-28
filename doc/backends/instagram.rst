Instagram
=========
Instagram uses OAuth v2 for Authentication

- Register a new application at the `Instagram API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      INSTAGRAM_CLIENT_ID = ''
      INSTAGRAM_CLIENT_SECRET = ''

- extra scopes can be defined by using::

    INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

*Note:*
Instagram only allows one callback url so you'll have to change your urls.py to
accomodate both ``/complete`` and ``/associate`` routes, for example by having
a single ``/associate`` url which takes a ``?complete=true`` parameter for the
cases when you want to complete rather than associate.

.. _Instagram API: http://instagr.am/developer/

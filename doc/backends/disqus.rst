DISQUS
=========
DISQUS uses OAuth v2 for Authentication

- Register a new application at the `DISQUS API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      DISQUS_CLIENT_ID = ''
      DISQUS_CLIENT_SECRET = ''

- extra scopes can be defined by using::

    DISQUS_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

*Note:*
DISQUS only allows one callback url so you'll have to change your urls.py to
accomodate both ``/complete`` and ``/associate`` routes, for example by having
a single ``/associate`` url which takes a ``?complete=true`` parameter for the
cases when you want to complete rather than associate.

.. _DISQUS AUTH API: http://disqus.com/api/docs/auth/
.. _DISQUS API: http://disqus.com/api/applications/

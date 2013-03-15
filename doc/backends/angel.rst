Angel List
=========
Angel uses OAuth v2 for Authentication

- Register a new application at the `Angel List API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      ANGEL_CLIENT_ID = ''
      ANGEL_CLIENT_SECRET = ''

- extra scopes can be defined by using::

    ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email message'}

*Note:*
Angel List does not currently support returning 'state' variable.

.. _Angel List API: https://angel.co/api/oauth/faq

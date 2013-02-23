Stackoverflow
======
Stackoverflow uses OAuth 2.0

- "Register For An App Key" at the `Stack Exchange API` site. Set your OAuth
  domain and application website settings.

- Add the ``Client Id``, ``Client Secret`` and ``Key`` values in settings::

    STACKOVERFLOW_CLIENT_ID = ''
    STACKOVERFLOW_CLIENT_SECRET = ''
    STACKOVERFLOW_KEY = ''

- You can ask for extra permissions with::

      STACKOVERFLOW_EXTENDED_PERMISSIONS = [...]

.. _Stack Exchange API: https://api.stackexchange.com/

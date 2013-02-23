Behance
=======
Behance uses OAuth2 for its auth mechanism.

- Register a new application at `Behance App Registration`_, set your
  application name, website and redirect URI.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      BEHANCE_CLIENT_ID = ''
      BEHANCE_CLIENT_SECRET = ''

- Also it's possible to define extra permissions with::

     BEHANCE_EXTENDED_PERMISSIONS = [...]

Check available permissions at `Possible Scopes`_. Also check the rest of their
doc at `Behance Developer Documentation`_.

.. _Behance App Registration: http://www.behance.net/dev/register
.. _Possible Scopes: http://www.behance.net/dev/authentication#scopes
.. _Behance Developer Documentation: http://www.behance.net/dev

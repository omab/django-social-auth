GitHub
======
Github works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, and

- fill ``App Id`` and ``App Secret`` values in the settings::

      GITHUB_APP_ID = ''
      GITHUB_API_SECRET = ''

- also it's possible to define extra permissions with::

     GITHUB_EXTENDED_PERMISSIONS = [...]


.. _GitHub Developers: https://github.com/account/applications/new

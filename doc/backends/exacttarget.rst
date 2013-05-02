ExactTarget
^^^^^^^^^^^

ExactTarget uses a JWT for authentication.

To use this backend, you must install the package ``pyjwt`` (`Github`_)

- Register a new application at `code.exacttarget.com`_, and

- Set the Logon URL to http://[your domain]/social/complete/exacttarget/

- fill ``Application Signature`` values in your django settings::

      EXACTTARGET_APP_SIGNATURE = ''

.. _code.exacttarget.com: http://code.exacttarget.com
.. _Github: https://github.com/progrium/pyjwt/

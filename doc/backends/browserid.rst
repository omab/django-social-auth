---------
BrowserID
---------
Support for BrowserID_ is possible by posting the ``assertion`` code to
``/complete/browserid/`` URL.

The setup doesn't need any setting, just the usual BrowserID_ javascript
include in your document and the needed mechanism to trigger the POST to
`django-social-auth`_.

Check the second "Use Case" for an implementation example.

.. _django-social-auth: https://github.com/omab/django-social-auth
.. _BrowserID: https://browserid.org

Facebook
========

Facebook works similar to Twitter but it's simpler to setup and
redirect URL is passed as a parameter when issuing an authorization.
Further documentation at `Facebook development resources`_:

- Register a new application at `Facebook App Creation`_, and

- fill **App Id** and **App Secret** values in values::

      FACEBOOK_APP_ID
      FACEBOOK_API_SECRET

- also it's possible to define extra permissions with::

     FACEBOOK_EXTENDED_PERMISSIONS = [...]

If you define a redirect URL in Facebook setup page, be sure to not
define http://127.0.0.1:8000 or http://localhost:8000 because it won't
work when testing. Instead I define http://myapp.com and setup a mapping
on /etc/hosts or use dnsmasq_.


.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/

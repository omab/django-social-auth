Twitter
=======

Twitter offers per application keys named ``Consumer Key`` and ``Consumer Secret``.
To enable Twitter these two keys are needed. Further documentation at
`Twitter development resources`_:

- Register a new application at `Twitter App Creation`_,

- mark the **Yes, use Twitter for login** checkbox, and

- fill **Consumer Key** and **Consumer Secret** values::

      TWITTER_CONSUMER_KEY
      TWITTER_CONSUMER_SECRET

- You need to specify an URL callback or the application will be marked as
  Client type instead of the Browser. Almost any dummy value will work if
  you plan some test.

.. _Twitter development resources: http://dev.twitter.com/pages/auth
.. _Twitter App Creation: http://twitter.com/apps/new

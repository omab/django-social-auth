Tokens
------

Almost every service covered provide some kind of API that is protected with
``access_token`` or token pairs (like `Twitter OAuth keys`_). These tokens are
gathered by the authentication mechanism and stored in
``UserSocialAuth.extra_data``.

``UserSocialAuth`` has a property named ``tokens`` to easilly access this
useful values, it will return a dictionary containing the tokens values.
A simple usage example::

    >>> from pprint import pprint
    >>> from social_auth.models import UserSocialAuth
    >>> instance = UserSocialAuth.objects.filter(provider='twitter').get(...)
    >>> pprint(instance.tokens)
    {u'oauth_token': u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
     u'oauth_token_secret': u'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'}
    >>> instance = UserSocialAuth.objects.filter(provider='facebook').get(...)
    >>> pprint(instance.tokens)
    {u'access_token': u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}

.. _Twitter OAuth keys: https://dev.twitter.com/docs/auth/authorizing-request

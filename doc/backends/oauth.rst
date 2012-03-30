OAuth
=====

OAuth_ communication demands a set of keys exchange to validate the client
authenticity prior to user approbation. Twitter, Facebook and Orkut
facilitates these keys by application registration, Google works the same,
but provides the option for unregistered applications.

Check next sections for details.

OAuth_ backends also can store extra data in ``UserSocialAuth.extra_data``
field by defining a set of values names to retrieve from service response.

Settings is per backend and it's name is dynamically checked using uppercase
backend name as prefix::

    <uppercase backend name>_EXTRA_DATA

Example::

    FACEBOOK_EXTRA_DATA = [(..., ...)]

Settings must be a list of tuples mapping value name in response and value
alias used to store. A third value (boolean) is supported to, it's purpose is
to signal if the value should be discarded if it evaluates to ``False``, this
is to avoid replacing old (needed) values when they don't form part of current
response. If not present, then this check is avoided and the value will replace
any data.


.. _OAuth: http://oauth.net/

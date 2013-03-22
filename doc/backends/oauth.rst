OAuth
=====

OAuth_ communication demands a set of keys exchange to validate the client
authenticity prior to user approbation. Twitter, Facebook and Orkut
facilitates these keys by application registration, Google works the same,
but provides the option for unregistered applications.

Check next sections for details.

OAuth_ backends also can store extra data in ``UserSocialAuth.extra_data``
field by defining a set of values names to retrieve from service response.

Settings is per backend and its name is dynamically checked using uppercase
backend name as prefix::

    <uppercase backend name>_EXTRA_DATA

For example, a subset of the data GitHub's provider returns is::

    {
        'avatar_url': 'https://secure.gravatar.com/avatar/[...]',
        'created_at': '2009-02-11T02:18:24Z',
        'email': 'john@example.com',
        'id': 53537,
        'login': 'github_user'
        'name': 'Johnny Codemore',
        [...]
    }

To add the avatar and login items to ``UserSocialAuth.extra_data``, you would
define the following in ``settings.py``::

    GITHUB_EXTRA_DATA = [
        ('avatar_url', 'avatar'),
        ('login', 'login'),
    ]

Settings must be a list of tuples mapping value name in response and value's
alias used in ``UserSocialAuth.extra_data``.  The alias is used to normalize
data access across multiple backends.  In the example above, GitHub sends
back a URL for the avatar in the field ``avatar_url``.  Alternatively, another
backend can send it as ``avatar``, or ``gravatar``.  By using a single name,
``avatar``, within ``UserSocialAuth.extra_data`` your application can more
easily use this information.

A third value (boolean) is supported, its purpose is to signal if the value
should be discarded if it evaluates to ``False``, this is to avoid replacing
old (needed) values when they don't form part of current response. If not
present, then this check is avoided and the value will replace any data.


.. _OAuth: http://oauth.net/

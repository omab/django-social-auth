LinkedIn
========

LinkedIn setup is similar to any other OAuth service. To request extra fields
using `LinkedIn fields selectors`_ just define this setting::

    LINKEDIN_EXTRA_FIELD_SELECTORS = [...]

with the needed fields selectors, also define LINKEDIN_EXTRA_DATA properly, that
way the values will be stored in ``UserSocialAuth.extra_data`` field.

By default ``id``, ``first-name`` and ``last-name`` are requested and stored.

If you want to request a user's email address, you'll need specify that your
application needs access to the email address using the ``r_emailaddress``
scope parameter. Also note that until they figure out a migration plan, they
require new API keys from the LinkedIn API (Issued after August 6th, 2012).

LinkedIn emulates the scope parameter of OAuth2 to specify user privileges.
Check here for `scope possibilities`_ if you need more than just the basic
profile.

These are declared as a list by defining this setting::

    LINKEDIN_SCOPE = ['r_basicprofile', ...]
    

.. _LinkedIn fields selectors: http://developer.linkedin.com/docs/DOC-1014
.. _scope possibilities: https://developer.linkedin.com/documents/authentication#granting

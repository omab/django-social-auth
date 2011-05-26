Miscellaneous
=============

Join to django-social-auth_ community on Convore_ and bring any questions or
suggestions that will improve this app.


South_ users should add this rule to enable migrations::

    try:
        import south
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], ["^social_auth\.fields\.JSONField"])
    except:
        pass


.. _South: http://south.aeracode.org/
.. _django-social-auth: https://convore.com/django-social-auth/
.. _Convore: https://convore.com/

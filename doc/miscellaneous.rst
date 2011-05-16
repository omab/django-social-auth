Miscellaneous
=============

South_ users should add this rule to enable migrations::
    try:
        import south
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], ["^social_auth\.fields\.JSONField"])
    except:
        pass


.. _South: http://south.aeracode.org/

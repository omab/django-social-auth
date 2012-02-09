Use Cases
=========

Some particular use cases are listed below.

1. Use social auth just for account association (no login)::

    urlpatterns += patterns('',
        url(r'^associate/(?P<backend>[^/]+)/$', associate,
            name='socialauth_associate_begin'),
        url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
            name='socialauth_associate_complete'),
        url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect,
            name='socialauth_disconnect'),
        url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
            disconnect, name='socialauth_disconnect_individual'),
    )

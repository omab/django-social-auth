"""URLs module"""
from django.conf.urls.defaults import patterns, url

from social_auth.views import auth, complete, associate, associate_complete, \
                              disconnect


urlpatterns = patterns('',
    # authentication
    url(r'^login/(?P<backend>[^/]+)/$', auth,
        name='socialauth_begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', complete,
        name='socialauth_complete'),

    # association
    url(r'^associate/(?P<backend>[^/]+)/$', associate,
        name='socialauth_associate_begin'),
    url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
        name='socialauth_associate_complete'),

    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect,
        name='socialauth_disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
        disconnect, name='socialauth_disconnect_individual'),
)

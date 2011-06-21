"""URLs module"""
from django.conf.urls.defaults import patterns, url

from social_auth.views import auth, complete, associate, associate_complete, \
                              disconnect


urlpatterns = patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', auth, name='begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'),
    url(r'^associate/(?P<backend>[^/]+)/$', associate, name='associate_begin'),
    url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
        name='associate_complete'),
    url(r'^disconnect/(?P<backend>[^/]+)/$', disconnect, name='disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>\d+)/$', disconnect,
        name='disconnect_individual'),
)

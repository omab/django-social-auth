"""URLs module"""
from django.conf.urls.defaults import patterns, url

from .views import auth, complete, associate, associate_complete


urlpatterns = patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', auth, name='begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'),
    url(r'^associate/(?P<backend>[^/]+)/$', associate, name='associate_begin'),
    url(r'^associate/complete/(?P<backend>[^/]+)/$', associate_complete,
        name='associate_complete'),
)

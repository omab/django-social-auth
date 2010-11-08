from django.conf.urls.defaults import patterns, url

from .views import auth, complete


urlpatterns = patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', auth, name='begin'), 
    url(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'), 
)

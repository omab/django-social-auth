from django.conf.urls.defaults import patterns, url

from .views import home, done, logout, auth, complete


urlpatterns = patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', auth, name='begin'), 
    url(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'), 

    # demo urls
    url(r'^$', home, name='home'), 
    url(r'^done/$', done, name='done'), 
    url(r'^logout/$', logout, name='logout'), 
)

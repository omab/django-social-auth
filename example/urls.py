from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from app.views import home, done, logout, error


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)

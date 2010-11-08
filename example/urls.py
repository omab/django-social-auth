from django.conf.urls.defaults import *
from django.contrib import admin

from app.views import home, done, logout


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'), 
    url(r'^done/$', done, name='done'), 
    url(r'^logout/$', logout, name='logout'), 
    url(r'', include('social_auth.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)

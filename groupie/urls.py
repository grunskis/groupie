from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'groupie.views.home', name='home'),
    # url(r'^groupie/', include('groupie.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

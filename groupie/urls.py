from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^(?P<vote_hash>[a-zA-Z0-9]{8})$', 'groupie.app.views.voting', name='voting'),
    url(r'^$', 'groupie.app.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
)

# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from nablaweb.news.feeds import RecentNews

from django.contrib import admin
admin.autodiscover()

from settings import GLOBAL_MEDIA_DIRS, MEDIA_ROOT, STATIC_URL

urlpatterns = patterns('',
    (r'^$', include('news.urls')),
    url(r'^login/$', 'accounts.views.login_user', name='auth_login'),
    url(r'^logout/$', 'accounts.views.logout_user', name='auth_logout'),
    (r'^nyheter/', include('nablaweb.news.urls')),
    (r'^bedpres/', include('nablaweb.bedpres.urls')),
    (r'^arrangement/', include('nablaweb.events.urls')),
    (r'^brukere/', include('accounts.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^stillinger/', include('jobs.urls')),
    (r'^komite/', include('com.urls')),
    (r'^gallery/', include('gallery.urls')),  # Kan ikke endres pga hardkoding i gallery-appen
    (r'^sitater/', include('quotes.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^nabladet/', include('nabladet.urls')),
    (r'^kommentarer/', include('django.contrib.comments.urls')),
    (r'^poll/', include('poll.urls')),

    # For å dele filer under utviklingen.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': GLOBAL_MEDIA_DIRS[0]}),
    (r'^media/(?P<path>.*)$',  'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    # Redirecte til favicon
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': STATIC_URL + 'img/favicon.ico'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     
     (r'^forum/', include('pybb.urls', namespace='pybb')),
     (r'^irc/', include('irc.urls')),
     url(r'^feed/$', RecentNews()),
)

urlpatterns += staticfiles_urlpatterns()

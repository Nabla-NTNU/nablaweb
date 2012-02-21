# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from settings import GLOBAL_MEDIA_DIRS, MEDIA_ROOT, STATIC_URL

urlpatterns = patterns('',
    # Example:
    # (r'^nablaweb/', include('nablaweb.foo.urls')),
    
    (r'^$', include('news.urls')),
    (r'^login/$', 'accounts.views.login_user'),
    (r'^logout/$', 'accounts.views.logout_user'),
    (r'^nyheter/', include('nablaweb.news.urls')),	
    (r'^arrangement/', include('nablaweb.events.urls')),
    (r'^bedpres/', include('nablaweb.bedpres.urls')),
    (r'^brukere/', include('accounts.urls')),
    (r'^avatar/', include('avatar.urls')),    
    (r'^stillinger/', include('jobs.urls')),
    (r'^komite/', include('com.urls')),
    (r'^gallery/', include('gallery.urls')), # Kan ikke endres pga hardkoding i gallery-appen
    (r'^sitater/', include('quotes.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^nabladet/', include('nabladet.urls')),
    (r'^kommentarer/', include('django.contrib.comments.urls')),
    
    # For å dele static files på /static/ under DEBUG
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': GLOBAL_MEDIA_DIRS[0]}),

    # For å dele media files på /media/ under DEBUG
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': MEDIA_ROOT}),

    # Redirecte til favicon
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': STATIC_URL + 'img/favicon.ico'}),
    
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

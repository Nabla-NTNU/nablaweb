from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^nablaweb/', include('nablaweb.foo.urls')),
    
    (r'^$', include('homepage.urls')),
    (r'^login/$', 'accounts.views.login_user'),
    (r'^logout/$', 'accounts.views.logout_user'),
    (r'^nyheter/', include('nablaweb.news.urls')),	
    (r'^arrangement/', include('nablaweb.events.urls')),
    (r'^bedpres/', include('nablaweb.bedpres.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^avatar/', include('avatar.urls')),    
    (r'^stillinger/', include('jobs.urls')),
    (r'^komite/', include('com.urls')),
    (r'^gallery/', include('gallery.urls')), # Kan ikke endres pga hardkoding i gallery-appen
    (r'^sitat/', include('quotes.urls')),
    
    # For aa vise bilder i runserver
    #(r'^nabla_media/(?P<path>.*)$','django.views.static.serve',{'document_root': getattr(settings, 'MEDIA_ROOT', None)}),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

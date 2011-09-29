from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^nablaweb/', include('nablaweb.foo.urls')),
    
    (r'^$', 'views.index'),
    (r'^login/$', 'accounts.views.login_user'),
    (r'^logout/$', 'accounts.views.logout_user'),
    (r'^nyheter/', include('nablaweb.news.urls')),	
    (r'^medlemmer/(?P<username>\w+)/', 'accounts.views.view_member_profile'),
    (r'^arrangement/', include('nablaweb.events.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^avatar/', include('avatar.urls')),
    # Midlertidige urler (kommer mest sannsynlig til aa forandres)
    (r'^profile/edit/$', 'accounts.views.edit_profile'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)

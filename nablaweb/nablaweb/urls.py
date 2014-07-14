# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from news.feeds import RecentNews

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    (r'^$', include('news.urls')),
    url(r'^login/$', 'accounts.views.login_user', name='auth_login'),
    url(r'^logout/$', 'accounts.views.logout_user', name='auth_logout'),
    url(r'^passord/reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^nyheter/', include('news.urls')),
    (r'^bedpres/', include('bedpres.urls')),
    (r'^arrangement/', include('events.urls')),
    (r'^brukere/', include('accounts.urls')),
    (r'^stillinger/', include('jobs.urls')),
    (r'^komite/', include('com.urls')),
    (r'^sitater/', include('quotes.urls')),
    (r'^nabladet/', include('nabladet.urls')),
    #(r'^referater/', include('meeting_records.urls')),
    (r'^kommentarer/', include('django.contrib.comments.urls')),
    (r'^poll/', include('poll.urls')),
    (r'^skraattcast/', include('skraattcast.urls')),

    # For å dele filer under utviklingen.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$',  'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Redirecte til favicon
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

    #(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^feed/$', RecentNews()),
    (r'^search/', include('search.urls')),
)

urlpatterns += staticfiles_urlpatterns()

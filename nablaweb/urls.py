# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.views.generic import RedirectView, TemplateView
from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm
from content.feeds.news import RecentNews
# nødvendig for django-wiki
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

from filebrowser.sites import site


from accounts.urls import login_urls
from .views import FrontPageView


admin.autodiscover()

urlpatterns = [
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^', include('content.urls')),
    url(r'^bedpres/', include('bedpres.urls')),
    url(r'^brukere/', include('accounts.urls')),
    url(r'^', include(login_urls)),
    url(r'^stillinger/', include('jobs.urls')),
    url(r'^komite/', include('com.urls')),
    url(r'^nabladet/', include('nabladet.urls')),
    url(r'^referater/', include('meeting_records.urls')),
    url(r'^kommentarer/', include('django_comments.urls')),
    url(r'^poll/', include('poll.urls')),
    url(r'^podcast/', include('podcast.urls')),
    url(r'^', include('interactive.urls')),
    url(r'^likes/', include('likes.urls')),
    url(r'^utveksling/', include('exchange.urls')),


    # For å dele filer under utviklingen selv om DEBUG=False
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$',  serve, {'document_root': settings.MEDIA_ROOT}),

    # Redirecte til favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^feed/$', RecentNews()),
    url(r'^search/$',
        search_view_factory(view_class=SearchView,
                            form_class=SearchForm),
        name='haystack_search'),
]

urlpatterns += staticfiles_urlpatterns()

# django-wiki
urlpatterns += [
    url(r'^wiki/notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern())
]

if settings.DEBUG:
    urlpatterns += [
         url(r'^500.html/$', TemplateView.as_view(template_name='500.html')),
         url(r'^404.html/$', TemplateView.as_view(template_name='404.html')),
    ]

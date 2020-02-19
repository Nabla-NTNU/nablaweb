import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView, TemplateView
from django.views.static import serve

import django_nyt.urls
import filebrowser.sites
import wiki.urls
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory

from nablapps.accounts.urls import login_urls
from nablapps.core.views import FrontPageView
from nablapps.nabladet.views import serve_nablad
from nablapps.news.feeds import RecentNews

admin.autodiscover()


## For search
sqs = SearchQuerySet().order_by('-pub_date')

urlpatterns = [
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^', include(login_urls)),
    url(r'^', include('nablapps.interactive.urls')),
    url(r'^admin/filebrowser/', filebrowser.sites.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^album/', include('nablapps.album.urls')),
    url(r'^application/', include('nablapps.apply_committee.urls')),
    url(r'^arrangement/', include('nablapps.events.urls')),
    url(r'^blogg/', include('nablapps.blog.urls')),
    url(r'^brukere/', include('nablapps.accounts.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),
    url(r'^feed/$', RecentNews()),
    url(r'^komite/', include('nablapps.com.urls')),
    url(r'^kommentarer/', include('django_comments.urls')),
    url(r'^nabladet/', include('nablapps.nabladet.urls')),
    url(r'^nyheter/', include('nablapps.news.urls')),
    url(r'^officebeer/', include('nablapps.officeBeer.urls')),
    url(r'^podcast/', include('nablapps.podcast.urls')),
    url(r'^poll/', include('nablapps.poll.urls')),
    url(r'^referater/', include('nablapps.meeting_records.urls')),
    url(r'^qrTickets/', include('nablapps.qrTickets.urls')),
    url(r'^search/$', search_view_factory(view_class=SearchView,
                                          form_class=ModelSearchForm,
                                          searchqueryset=sqs), name='haystack_search'),
    url(r'^shop/', include('nablapps.nablashop.urls', namespace='nablashop')),
    url(r'^stillinger/', include('nablapps.jobs.urls')),
    url(r'^utveksling/', include('nablapps.exchange.urls')),
    url(r'^contact/', include('nablapps.contact.urls')),
    url(r'^wiki/notifications/', django_nyt.urls.get_pattern()),
    url(r'^wiki/', wiki.urls.get_pattern()),
    url(r'^om-nabla/', include('nablapps.core.urls')),
    path('forum/', include('nablapps.nablaforum.urls')),

    # For å ta i bruk robots.txt
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),

    # Del filer (Husk manage.py collectstatic for static filer når DEBUG=False)
    url(r'^media/nabladet/(?P<path>.*)$', serve_nablad),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^500.html/$', TemplateView.as_view(template_name='500.html')),
        url(r'^404.html/$', TemplateView.as_view(template_name='404.html')),
        url(r'^protected_media/(?P<path>.*)$', serve,
            {'document_root': os.path.join(settings.PROTECTED_MEDIA_ROOT, 'nabladet')}, name='serve_nablad_debug'),
    ]

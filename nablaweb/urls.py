import django_nyt.urls
import filebrowser.sites
import wiki.urls

from nablapps.news.feeds import RecentNews
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.views.generic import RedirectView, TemplateView

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from nablapps.accounts.urls import login_urls
from nablapps.nabladet.views import serve_nablad
from .views import FrontPageView

admin.autodiscover()


## For search
sqs = SearchQuerySet().order_by('-pub_date')

urlpatterns = [
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^', include(login_urls)),
    url(r'^', include('nablapps.interactive.urls')),
    url(r'^admin/filebrowser/', include(filebrowser.sites.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^album/', include('contentapps.album.urls')),
    url(r'^arrangement/', include('nablapps.events.urls')),
    url(r'^bedpres/', include('nablapps.bedpres.urls')),
    url(r'^blogg/', include('contentapps.blog.urls')),
    url(r'^brukere/', include('nablapps.accounts.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),
    url(r'^feed/$', RecentNews()),
    url(r'^komite/', include('nablapps.com.urls')),
    url(r'^kommentarer/', include('django_comments.urls')),
    url(r'^nabladet/', include('nablapps.nabladet.urls')),
    url(r'^nyheter/', include('nablapps.news.urls')),
    url(r'^podcast/', include('nablapps.podcast.urls')),
    url(r'^poll/', include('nablapps.poll.urls')),
    url(r'^referater/', include('nablapps.meeting_records.urls')),
    url(r'^search/$', search_view_factory(view_class=SearchView,
                                          form_class=ModelSearchForm,
                                          searchqueryset=sqs), name='haystack_search'),
    url(r'^shop/', include('nablapps.nablashop.urls', namespace='nablashop')),
    url(r'^stillinger/', include('nablapps.jobs.urls')),
    url(r'^utveksling/', include('nablapps.exchange.urls')),
    url(r'^wiki/notifications/', django_nyt.urls.get_pattern()),
    url(r'^wiki/', wiki.urls.get_pattern()),

    # For å ta i bruk robots.txt
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),

    # Del filer (Husk manage.py collectstatic for static filer når DEBUG=False)
    url(r'^media/nabladet/(?P<path>.*)$', serve_nablad, {'document_root': settings.MEDIA_ROOT + '/nabladet/'}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns += [
         url(r'^500.html/$', TemplateView.as_view(template_name='500.html')),
         url(r'^404.html/$', TemplateView.as_view(template_name='404.html')),
    ]

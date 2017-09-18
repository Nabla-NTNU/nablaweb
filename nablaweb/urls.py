import django_nyt.urls
import filebrowser.sites
import wiki.urls

from content.feeds.news import RecentNews
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.views.generic import RedirectView, TemplateView

from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm

from nablapps.accounts.urls import login_urls
from .views import FrontPageView

admin.autodiscover()

urlpatterns = [
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^', include(login_urls)),
    url(r'^', include('nablapps.interactive.urls')),
    url(r'^', include('content.urls')),
    url(r'^admin/filebrowser/', include(filebrowser.sites.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bedpres/', include('nablapps.bedpres.urls')),
    url(r'^blogg/', include('contentapps.blog.urls')),
    url(r'^brukere/', include('nablapps.accounts.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),
    url(r'^feed/$', RecentNews()),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^komite/', include('nablapps.com.urls')),
    url(r'^kommentarer/', include('django_comments.urls')),
    url(r'^likes/', include('nablapps.likes.urls')),
    url(r'^nabladet/', include('nablapps.nabladet.urls')),
    url(r'^podcast/', include('nablapps.podcast.urls')),
    url(r'^poll/', include('nablapps.poll.urls')),
    url(r'^referater/', include('nablapps.meeting_records.urls')),
    url(r'^search/$', search_view_factory(view_class=SearchView,
                                          form_class=SearchForm), name='haystack_search'),
    url(r'^shop/', include('nablapps.nablashop.urls', namespace='nablashop')),
    url(r'^stillinger/', include('nablapps.jobs.urls')),
    url(r'^utveksling/', include('nablapps.exchange.urls')),
    url(r'^wiki/notifications/', django_nyt.urls.get_pattern()),
    url(r'^wiki/', wiki.urls.get_pattern()),
]


if settings.DEBUG:
    urlpatterns += [
         url(r'^500.html/$', TemplateView.as_view(template_name='500.html')),
         url(r'^404.html/$', TemplateView.as_view(template_name='404.html')),
    ]
else:
    # Del filer selv om DEBUG=False. (Husk manage.py collectstatic for static filer)
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

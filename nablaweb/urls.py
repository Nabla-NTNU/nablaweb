import os

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
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
sqs = SearchQuerySet().order_by("-pub_date")

urlpatterns = [
    path("", FrontPageView.as_view(), name="front_page"),
    path("", include(login_urls)),
    path("", include("nablapps.interactive.urls")),
    path("admin/filebrowser/", filebrowser.sites.site.urls),
    path("admin/", admin.site.urls),
    path("album/", include("nablapps.album.urls")),
    path("application/", include("nablapps.apply_committee.urls")),
    path("arrangement/", include("nablapps.events.urls")),
    path("blogg/", include("nablapps.blog.urls")),
    path("brukere/", include("nablapps.accounts.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(
            url=settings.STATIC_URL + "img/favicon.ico", permanent=True
        ),
    ),
    path("feed/", RecentNews()),
    path("komite/", include("nablapps.com.urls")),
    path("kommentarer/", include("django_comments.urls")),
    path("nabladet/", include("nablapps.nabladet.urls")),
    path("nyheter/", include("nablapps.news.urls")),
    path("officebeer/", include("nablapps.officeBeer.urls")),
    path("podcast/", include("nablapps.podcast.urls")),
    path("poll/", include("nablapps.poll.urls")),
    path("referater/", include("nablapps.meeting_records.urls")),
    path("qrTickets/", include("nablapps.qrTickets.urls")),
    path(
        "search/",
        search_view_factory(
            view_class=SearchView, form_class=ModelSearchForm, searchqueryset=sqs
        ),
        name="haystack_search",
    ),
    path("shop/", include("nablapps.nablashop.urls", namespace="nablashop")),
    path("stillinger/", include("nablapps.jobs.urls")),
    path("utveksling/", include("nablapps.exchange.urls")),
    path("contact/", include("nablapps.contact.urls")),
    path("wiki/notifications/", django_nyt.urls.get_pattern()),
    path("wiki/", wiki.urls.get_pattern()),
    path("om-nabla/", include("nablapps.core.urls")),
    path("forum/", include("nablapps.nablaforum.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # For å ta i bruk robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # Del filer (Husk manage.py collectstatic for static filer når DEBUG=False)
    path("media/nabladet/<path:path>/", serve_nablad),
    path("media/<path:path>/", serve, {"document_root": settings.MEDIA_ROOT}),
    path("static/<path:path>/", serve, {"document_root": settings.STATIC_ROOT}),
    path("api-auth/", include("rest_framework.urls")),
]


if settings.DEBUG:
    urlpatterns += [
        path("500.html/", TemplateView.as_view(template_name="500.html")),
        path("404.html/", TemplateView.as_view(template_name="404.html")),
        path(
            "protected_media/<path:path>/",
            serve,
            {"document_root": os.path.join(settings.PROTECTED_MEDIA_ROOT, "nabladet")},
            name="serve_nablad_debug",
        ),
    ]

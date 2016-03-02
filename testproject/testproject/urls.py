
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from content.feeds.news import RecentNews
import content.urls
from django_nyt.urls import get_pattern as get_nyt_pattern


urlpatterns = [
    url(r'^login/$',
        login,
        {'template_name': 'admin/login.html'}
        ),
    url(r'^logout/$', logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(content.urls)),
    url(r'^feed/$', RecentNews()),
    url(r'^comments/', include('django_comments.urls')),

    # Dummyview to fix a reverse lookup error on 'member_profile'
    url(r'^userprofile/(?P<username>\w+)$',
        RedirectView.as_view(permanent=False, url="/"),
        name="member_profile"),

    url(r'^notifications/', get_nyt_pattern()),
]

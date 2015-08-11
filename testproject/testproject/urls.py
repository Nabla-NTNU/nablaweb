
from django.conf.urls import include, url
from django.contrib import admin
from content.feeds.news import RecentNews
import content.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(content.urls)),
    url(r'^feed/$', RecentNews()),
]

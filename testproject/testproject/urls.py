from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from contentapps.news.feeds import RecentNews


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^login/$',
        login,
        {'template_name': 'admin/login.html'}
        ),
    url(r'^logout/$', logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^album/', include('contentapps.album.urls')),
    url(r'^blogg/', include('contentapps.blog.urls')),
    url(r'^arrangement/', include('contentapps.events.urls')),
    url(r'^nyheter/', include('contentapps.news.urls')),
    url(r'^feed/$', RecentNews()),
    url(r'^comments/', include('django_comments.urls')),
]

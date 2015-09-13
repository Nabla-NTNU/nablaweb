
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from content.feeds.news import RecentNews
import content.urls

urlpatterns = [
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'admin/login.html'}
        ),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(content.urls)),
    url(r'^feed/$', RecentNews()),
    url(r'^comments/', include('django_comments.urls')),

    # Dummyview to fix a reverse lookup error on 'member_profile'
    url(r'^userprofile/(?P<username>\w+)$',
        RedirectView.as_view(permanent=False, url="/"),
        name="member_profile"),

]

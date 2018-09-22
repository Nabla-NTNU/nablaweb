"""
Urls for testproject for content
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.static import serve
from django.views.generic import TemplateView
from contentapps.image.views import view_markdown


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^album/', include('contentapps.album.urls')),
    url(r'^blogg/', include('contentapps.blog.urls')),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}, name="auth_login"),
    url(r'^logout/$', logout),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^markdowntest/$', view_markdown),
]

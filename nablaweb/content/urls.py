# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import AlbumOverview, AlbumView

urlpatterns = patterns('content.views',
    url(r'^album/$',
        AlbumOverview.as_view(),
        name='albums'),
    url(r'^album/(?P<pk>\d{1,8})/(?P<num>\d{1,8})',
        AlbumView.as_view(),
        name='album')
)

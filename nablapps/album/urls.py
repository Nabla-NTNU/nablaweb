"""
Urls for album app
"""
from django.conf.urls import url
from .views import (
    AlbumList,
    AlbumImageView,
    AlbumOverview,
)

urlpatterns = [
    url(r'^$',
        AlbumList.as_view(),
        name='albums'),
    url(r'^(?P<pk>\d{1,8})/(?P<num>\d{1,8})/$',
        AlbumImageView.as_view(),
        name='album_image'),
    url(r'^(?P<pk>\d{1,8})/$',
        AlbumOverview.as_view(),
        name='album'),
]

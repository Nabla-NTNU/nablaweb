from django.conf.urls import url
from .views import (
    AlbumList,
    AlbumImageView,
    AlbumOverview,
)

urlpatterns = [
    url(r'^album/$',
        AlbumList.as_view(),
        name='albums'),
    url(r'^album/(?P<pk>\d{1,8})/(?P<num>\d{1,8})/$',
        AlbumImageView.as_view(),
        name='album_image'),
    url(r'^album/(?P<pk>\d{1,8})/$',
        AlbumOverview.as_view(),
        name='album'),
]

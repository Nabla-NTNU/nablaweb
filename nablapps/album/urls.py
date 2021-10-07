"""
Urls for album app
"""
from django.urls import path

from .views import AlbumImageView, AlbumList, AlbumOverview

urlpatterns = [
    path("", AlbumList.as_view(), name="albums"),
    path("<int:pk>/<int:num>/", AlbumImageView.as_view(), name="album_image",),
    path("<int:pk>/", AlbumOverview.as_view(), name="album"),
]

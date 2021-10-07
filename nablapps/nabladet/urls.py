"""
Urls for nabladet app
"""
from django.urls import path

from .views import NabladDetailView, NabladList

urlpatterns = [
    path("", NabladList.as_view(), name="nablad_list"),
    path(
        "<int:pk>/<str:slug>/",
        NabladDetailView.as_view(),
        name="nablad_detail",
    ),
]

"""
Urls for nabladet app
"""
from django.conf.urls import url

from .views import NabladDetailView, NabladList

urlpatterns = [
    url(r"^$", NabladList.as_view(), name="nablad_list"),
    url(
        r"^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$",
        NabladDetailView.as_view(),
        name="nablad_detail",
    ),
]

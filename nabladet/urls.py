# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import NabladListView, NabladDetailView

urlpatterns = [
    url(r'^$',
        NabladListView.as_view(),
        name='nablad_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        NabladDetailView.as_view(),
        name='nablad_detail'),
]

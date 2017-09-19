# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^nyheter/$',
        NewsListView.as_view(),
        name='news_list'),
    url(r'^nyheter/(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        NewsDetailView.as_view(),
        name='news_detail'),
]

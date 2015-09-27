# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import SeasonView, detail

urlpatterns = [
    url(r'^$', SeasonView.as_view(), name='season_view'),
    url(r'^season(?P<number>\d+)$', SeasonView.as_view(), name='season_view'),
    url(r'^(?P<podcast_id>\d+)/$', detail, name='podcast_detail'),
]

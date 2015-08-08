# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import SeasonView, detail

urlpatterns = \
    patterns('',
             url(r'^$', SeasonView.as_view(), name='season_view'),
             url(r'^season(?P<number>\d+)$', SeasonView.as_view(), name='season_view'),
             url(r'^(?P<podcast_id>\d+)/$', detail, name='podcast_detail'),
             )

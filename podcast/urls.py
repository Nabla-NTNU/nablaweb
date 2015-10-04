# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import SeasonView, PodcastDetailView

urlpatterns = \
    patterns('',
             url(r'^$', SeasonView.as_view(), name='season_view'),
             url(r'^season(?P<number>\d+)$', SeasonView.as_view(), name='season_view'),
             url(r'^(?P<pk>\d+)/$', PodcastDetailView.as_view(), name='podcast_detail'),
             )

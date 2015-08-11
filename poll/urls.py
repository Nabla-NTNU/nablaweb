# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import vote

urlpatterns = patterns('',
    url(r'^(?P<poll_id>\d+)/vote/$',
        vote,
        name="poll_vote"),
)

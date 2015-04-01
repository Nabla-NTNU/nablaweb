# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^(?P<poll_id>\d+)/vote/$', 'poll.views.vote'),
)

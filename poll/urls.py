# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import vote, UserPollsView, PollListView, CreateUserPollView, UpdateUserPollView, delete_poll

urlpatterns = [
    url(r'^(?P<poll_id>\d+)/vote/$',
        vote,
        name="poll_vote"),
    url(r'^brukeravstemninger/$',
        PollListView.as_view(),
        name="user_polls"),
    url(r'^bruker/$',
        UserPollsView.as_view(),
        name="poll_user"),
    url(r'^bruker/ny/$',
        CreateUserPollView.as_view(),
        name="poll_user_create"),
    url(r'^bruker/endre/(?P<pk>[\d]+)$',
        UpdateUserPollView.as_view(),
        name="poll_user_update"),
    url(r'^bruker/slett/(?P<poll_id>[\d]+)$',
        delete_poll,
        name="poll_user_delete"),
]

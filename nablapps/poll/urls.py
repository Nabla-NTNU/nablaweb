"""
Urls for poll app
"""

from django.urls import path

from .views import (
    CreateUserPollView,
    DeleteUserPollView,
    PollListView,
    UserPollsView,
    vote,
)

urlpatterns = [
    path("<int:poll_id>/vote/", vote, name="poll_vote"),
    path("brukeravstemninger/", PollListView.as_view(), name="user_polls"),
    path("bruker/", UserPollsView.as_view(), name="poll_user"),
    path("bruker/ny/", CreateUserPollView.as_view(), name="poll_user_create"),
    path(
        "bruker/slett/<int:pk>/",
        DeleteUserPollView.as_view(),
        name="poll_user_delete",
    ),
]

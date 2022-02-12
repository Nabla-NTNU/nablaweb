from django.urls import path

from .views import (  # submit_vote,
    AdminVoteEventList,
    CreateVoting,
    RegisterAttendanceView,
    UsersAPIView,
    VoteEventAPIView,
    VoteEventList,
    VoteEventPublicAPIView,
    VotingEdit,
    VotingEventList,
    VotingEventUserView,
    VotingList,
    VotingsAPIView,
    VotingsPublicAPIView,
)

apiurlpatterns = [
    path("api/<int:pk>/", VoteEventAPIView.as_view(), name="api-vote-event"),
    path("api/<int:pk>/users/", UsersAPIView.as_view(), name="api-users"),
    path("api/<int:pk>/votings/", VotingsAPIView.as_view(), name="api-votings"),
    path(
        "api/<int:pk>/public/votings/",
        VotingsPublicAPIView.as_view(),
        name="api-public-votings",
    ),
    path(
        "api/<int:pk>/public/",
        VoteEventPublicAPIView.as_view(),
        name="api-public-vote-event",
    ),
]

urlpatterns = [
    *apiurlpatterns,
    ### Admin views ###
    path("admin/", AdminVoteEventList.as_view(), name="voting-event-list"),
    path("admin/event/<int:pk>/list/", VotingList.as_view(), name="voting-list"),
    path(
        "admin/event/<int:pk>/attendance/",
        RegisterAttendanceView.as_view(),
        name="register",
    ),
    path(
        "admin/event/<int:pk>/create_voting/",
        CreateVoting.as_view(),
        name="create-voting",
    ),
    path(
        "admin/voting/<int:pk>/edit/",
        VotingEdit.as_view(),
        name="voting-edit",
    ),
    ### Public views ###
    path("event/<int:pk>", VotingEventUserView.as_view(), name="voting-event-user"),
    path(
        "",
        VoteEventList.as_view(),
        name="vote-event-list",
    ),
]

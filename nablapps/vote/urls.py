from django.urls import path

from .views import (  # submit_vote,
    ActiveVotingList,
    CreateVoting,
    RegisterAttendanceView,
    UsersAPIView,
    Vote,
    VoteEventAPIView,
    VoteEventPublicAPIView,
    VotingDetail,
    VotingEdit,
    VotingEventList,
    VotingEventUserView,
    VotingList,
    VotingsAPIView,
    VotingsPublicAPIView,
    activate_voting,
    deactivate_voting,
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
    path("admin/", VotingEventList.as_view(), name="voting-event-list"),
    path("admin/<int:pk>/list/", VotingList.as_view(), name="voting-list"),
    path(
        "admin/<int:pk>/attendance/", RegisterAttendanceView.as_view(), name="register"
    ),
    path("admin/<int:pk>/create_voting/", CreateVoting.as_view(), name="create-voting"),
    path(
        "admin/detail/<int:pk>/",
        VotingDetail.as_view(),
        name="voting-detail",
    ),
    path(
        "admin/edit/<int:pk>/",
        VotingEdit.as_view(),
        name="voting-edit",
    ),
    path(
        "activate/<int:pk>/<path:redirect_to>/", activate_voting, name="activate-voting"
    ),
    path(
        "deactivate/<int:pk>/<path:redirect_to>/",
        deactivate_voting,
        name="deactivate-voting",
    ),
    path("event/<int:pk>", VotingEventUserView.as_view(), name="voting-event-user"),
    path(
        "",
        ActiveVotingList.as_view(),
        name="active-voting-list",
    ),
    path("<int:pk>/", Vote.as_view(), name="voting-vote"),
    # path("<int:voting_id>/", submit_vote, name="submit-vote"),
]

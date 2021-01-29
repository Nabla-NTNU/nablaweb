from django.urls import path

from .views import (
    ActiveVotingList,
    CreateVoting,
    Vote,
    VotingDetail,
    VotingEventList,
    VotingList,
    activate_voting,
    deactivate_voting,
    submit_vote,
)

urlpatterns = [
    path("event_list/", VotingEventList.as_view(), name="voting-event-list"),
    path("event/<int:pk>/list/", VotingList.as_view(), name="voting-list"),
    path(
        "event/<int:pk>/active-list/",
        ActiveVotingList.as_view(),
        name="active-voting-list",
    ),
    path("event/<int:pk>/create_voting/", CreateVoting.as_view(), name="create-voting"),
    path(
        "detail/<int:pk>/<int:event_id>/", VotingDetail.as_view(), name="voting-detail"
    ),
    path("vote/<int:pk>/<int:event_id>/", Vote.as_view(), name="voting-vote"),
    path("vote/<int:pk>/<int:event_id>/submit/", submit_vote, name="submit-vote"),
    path("activate/<int:pk>/<int:event_id>/", activate_voting, name="activate-voting"),
    path(
        "deactivate/<int:pk>/<int:event_id>/",
        deactivate_voting,
        name="deactivate-voting",
    ),
]

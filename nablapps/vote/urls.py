from django.urls import path

from .views import (  # submit_vote,
    ActiveVotingList,
    CreateVoting,
    Vote,
    VotingDetail,
    VotingEdit,
    VotingEventList,
    VotingList,
    activate_voting,
    deactivate_voting,
)

urlpatterns = [
    path("admin/", VotingEventList.as_view(), name="voting-event-list"),
    path("admin/<int:pk>/list/", VotingList.as_view(), name="voting-list"),
    path("admin/<int:pk>/create_voting/", CreateVoting.as_view(), name="create-voting"),
    path("admin/detail/<int:pk>/", VotingDetail.as_view(), name="voting-detail",),
    path("admin/edit/<int:pk>/", VotingEdit.as_view(), name="voting-edit",),
    path(
        "activate/<int:pk>/<path:redirect_to>/", activate_voting, name="activate-voting"
    ),
    path(
        "deactivate/<int:pk>/<path:redirect_to>/",
        deactivate_voting,
        name="deactivate-voting",
    ),
    path("", ActiveVotingList.as_view(), name="active-voting-list",),
    path("<int:pk>/", Vote.as_view(), name="voting-vote"),
    # path("<int:voting_id>/", submit_vote, name="submit-vote"),
]

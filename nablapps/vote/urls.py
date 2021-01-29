from django.urls import path

from .views import VotingList, CreateVoting, VotingDetail, activate_voting, deactivate_voting, Vote, ActiveVotingList, submit_vote

urlpatterns = [
    path("list/", VotingList.as_view(), name="voting-list"),
    path("active-list/", ActiveVotingList.as_view(), name="active-voting-list"),
    path("create_voting/", CreateVoting.as_view(), name="create-voting"),
    path("detail/<int:pk>/", VotingDetail.as_view(), name="voting-detail"),
    path("vote/<int:pk>/", Vote.as_view(), name="voting-vote"),
    path("vote/<int:pk>/submit/", submit_vote, name="submit-vote"),
    path("activate/<int:pk>/", activate_voting, name="activate-voting"),
    path("deactivate/<int:pk>/", deactivate_voting, name="deactivate-voting"),
]

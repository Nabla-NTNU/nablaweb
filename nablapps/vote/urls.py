from django.urls import path

from .views import VotationList, CreateVotation, VotationDetail, activate_votation, deactivate_votation, Vote, ActiveVotationList, submit_vote

urlpatterns = [
    path("list/", VotationList.as_view(), name="votation-list"),
    path("active-list/", ActiveVotationList.as_view(), name="active-votation-list"),
    path("create_votation/", CreateVotation.as_view(), name="create-votation"),
    path("detail/<int:pk>/", VotationDetail.as_view(), name="votation-detail"),
    path("vote/<int:pk>/", Vote.as_view(), name="votation-vote"),
    path("vote/<int:pk>/submit/", submit_vote, name="submit-vote"),
    path("activate/<int:pk>/", activate_votation, name="activate-votation"),
    path("deactivate/<int:pk>/", deactivate_votation, name="deactivate-votation"),
]

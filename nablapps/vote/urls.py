from django.urls import path

from .views import VotationList, CreateVotation, VotationDetail, activate_votation, deactivate_votation, Vote

urlpatterns = [
    path("list/", VotationList.as_view(), name="votation-list"),
    path("create_votation/", CreateVotation.as_view(), name="create-votation"),
    path("detail/<int:pk>/", VotationDetail.as_view(), name="votation-detail"),
    path("vote/<int:pk>/", Vote.as_view(), name="votation-vote"),
    path("activate/<int:pk>/", activate_votation, name="activate-votation"),
    path("deactivate/<int:pk>/", deactivate_votation, name="deactivate-votation"),
]

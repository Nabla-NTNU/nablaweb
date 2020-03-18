from django.urls import path
from django.views.generic import RedirectView

from .views import CommitteeOverview, ShowBoard, ShowPage

urlpatterns = [
    path("komiteer", CommitteeOverview.as_view(), name="committee_overview"),
    path("", RedirectView.as_view(url="/", permanent=True)),
    path("<str:slug>/", ShowPage.as_view(), name="show_com_page"),
    path("om/<str:slug>/", ShowBoard.as_view(), name="show-board-page"),
]

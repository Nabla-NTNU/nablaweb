from django.conf.urls import url
from django.views.generic import RedirectView

from .views import CommitteeOverview, ShowBoard, ShowPage

urlpatterns = [
    url(r"^komiteer", CommitteeOverview.as_view(), name="committee_overview"),
    url(r"^$", RedirectView.as_view(url="/", permanent=True)),
    url(r"^(?P<slug>[\w\-\']{1,85})/$", ShowPage.as_view(), name="show_com_page"),
    url(r"^om/(?P<slug>[\w\-\']{1,85})/$", ShowBoard.as_view(), name="show-board-page"),
]

# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import ShowPage, CommitteeOverview
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^komiteer', CommitteeOverview.as_view(), name='committee_overview'),
    url(r'^$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^(?P<slug>\D{1,85})/$', ShowPage.as_view(), name='show_com_page'),
]

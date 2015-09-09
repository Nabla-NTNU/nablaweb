# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import ShowPage, CommitteeOverview
from django.views.generic import RedirectView

urlpatterns = patterns('',
                       url(r'^komiteer', CommitteeOverview.as_view(), name='committee_overview'),
                       (r'^$', RedirectView.as_view(url='/', permanent=True)),
                       url(r'^(?P<slug>\D{1,85})/$', ShowPage.as_view(), name='show_com_page'),
                       )

# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView

from content.views import ical_event

from .views import BedPresDetailView, BedPresRegisterUserView

urlpatterns = [

    url(r'^$', RedirectView.as_view(url='/arrangement/', permanent=True)),
    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        BedPresDetailView.as_view(),
        name='bedpres_detail'),

    # Bruker
    url(r'^(?P<pk>\d{1,8})/registration$',
        BedPresRegisterUserView.as_view(),
        name='bedpres_registration'),

    # Eksporter
    url(r'^(?P<bedpres_id>\d{1,8})/eksporter$', ical_event),
]

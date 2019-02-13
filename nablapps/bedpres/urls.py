"""Url patterns for Bedpres-app"""
from django.conf.urls import url
from django.views.generic import RedirectView

from .views import BedPresDetailView, BedPresRegisterUserView, ical_event

urlpatterns = [

    url(r'^$', RedirectView.as_view(url='/arrangement/', permanent=True)),
    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        BedPresDetailView.as_view(),
        name='bedpres_detail'),

    url(r'^(?P<pk>\d{1,8})/registration$',
        BedPresRegisterUserView.as_view(),
        name='bedpres_registration'),

    #url(r'^(?P<bedpres_id>\d{1,8})/eksporter$', ical_event, name='bedpres_ical_event'),

    url(r'^(?P<event_id>\d{1,8}).ics$',
        ical_event,
        name="bedpres_ical_event"),
]

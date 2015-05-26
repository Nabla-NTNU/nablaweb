# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import *
from .feeds import RecentEvents

urlpatterns = patterns('events.views',

    # Administrasjon
    url(r'^(?P<pk>\d{1,8})/admin2$',
        AdministerRegistrationsView.as_view(),
        name='event_admin'),

    # Offentlig
    url(r'^$',
        'calendar',
        name='event_list'),

    url(r'^(\d{4})/(\d{1,2})/$',
        'calendar',
        name='event_list'),

    # Bruker
    url(r'^mine$',
        UserEventView.as_view(),
        name="view_user_events"),

    url(r'^(?P<pk>\d{1,8})/registration$',
        RegisterUserView.as_view(),
        name='registration'),

    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        EventDetailView.as_view(),
        name='event_detail'),

    url(r'^reg/(?P<pk>\d{1,8})$',
        EventRegistrationsView.as_view(),
        name='event_registrations'),

    # Eksporter
    url(r'^(?P<event_id>\d{1,8}).ics$',
        ical_event,
        name="ical_event"),

    # RSS-feed
    url(r'^feed/$', RecentEvents(), name="event_feed"),
)

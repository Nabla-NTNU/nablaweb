# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from nablaweb.events.views import EventDetailView, EventListView, UserEventView, EventRegistrationsView
from nablaweb.events.feeds import RecentEvents

from django.contrib.auth.decorators import login_required
#from django.views.decorators.cache import cache_page

urlpatterns = patterns('nablaweb.events.views',

    # Administrasjon
#    (r'^opprett/$', EventFormPreview(form=EventForm)),
#    (r'^(?P<pk>\d{1,8})/endre$', EventFormPreview(form=EventForm)),
#    (r'^(?P<pk>\d{1,8})/slette$', EventDeleteView.as_view()),
    url(r'^(?P<pk>\d{1,8})/admin$',
        'administer',
        name='event_admin'),
 
    # Offentlig
    url(r'^$',
        'calendar',
        name='event_list'),

    url(r'^(\d{4})/(\d{1,2})/$',
        'calendar',
        name='event_list'),

    # Bruker
    url(r'^mine$', login_required(UserEventView.as_view()), name="view_user_events"),
    (r'^(?P<event_id>\d{1,8})/registrering$', 'register_user'),
    (r'^(?P<event_id>\d{1,8})/avregistrering$', 'deregister_user'),

    url(r'^(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        EventDetailView.as_view(context_object_name="event"),
        name='event_detail'),

    url(r'^reg/(?P<pk>\d{1,8})$',
        EventRegistrationsView.as_view(context_object_name="event"),
        name='event_registrations'),

    # Eksporter
    url(r'^(?P<event_id>\d{1,8}).ics$', 'ical_event', name="ical_event"),
    
    # RSS-feed
    url(r'^feed/$', RecentEvents()),
)

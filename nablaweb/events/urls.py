# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.events.models import Event
from nablaweb.events.forms import EventForm
from nablaweb.events.views import EventDetailView, EventListView, EventDeleteView, UserEventView


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
        EventListView.as_view(),
        name='event_list'),

    url(r'^(\d{4})/(\d{1,2})/$',
        EventListView.as_view(),
        name='event_list'),

    url(r'^(?P<pk>\d{1,8})/$',
        EventDetailView.as_view( context_object_name="event" ),
        name='event_detail'),

    # Bruker
    (r'^mine$', UserEventView.as_view()),
    (r'^(?P<event_id>\d{1,8})/registrering$', 'register_user'),

    # Eksporter
    (r'^(?P<event_id>\d{1,8})/eksporter$', 'ical_event'),
)

# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, UpdateView
from nablaweb.events.models import Event
from nablaweb.events.forms import EventForm, EventFormPreview
from nablaweb.events.views import EventUpdateView

urlpatterns = patterns('events.views',

    # Administrasjon
    (r'^opprett/$', EventFormPreview(form=EventForm)),
    (r'^(?P<pk>\d{1,8})/endre$', EventUpdateView.as_view()),
    (r'^(?P<event_id>\d{1,8})/admin$', 'administer'),
    (r'^(?P<event_id>\d{1,8})/slett$', 'delete'),

    # Offentlig
    (r'^$',
     ListView.as_view(model=Event,
                      queryset=Event.objects.all().order_by('-created_date')[:5],
                      context_object_name='content_list',)),
    url(r'^(?P<pk>\d{1,8})/$',
        DetailView.as_view(model=Event,
                           context_object_name='content',),
        name='event_detail',),

    # Bruker
    (r'^mine$', 'show_user'),
    (r'^(?P<event_id>\d{1,8})/registrering$', 'register_user'),

    # Eksporter
    (r'^(?P<event_id>\d{1,8})/eksporter$', 'ical_event'),
)

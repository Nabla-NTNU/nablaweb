# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from nablaweb.events.models import Event


urlpatterns = patterns('events.views',

    # Administrasjon
    (r'^opprett/$', 'create_or_edit_event'),
    (r'^(?P<event_id>\d{1,8})/admin$', 'administer'),
    (r'^(?P<event_id>\d{1,8})/endre$', 'create_or_edit_event'),
    (r'^(?P<event_id>\d{1,8})/slett$', 'delete'),

    # Offentlig
    (r'^$',
     ListView.as_view(model=Event,
                      queryset=Event.objects.all().order_by('-created_date')[:5],
                      context_object_name='content_list',)),
    (r'^(?P<pk>\d{1,8})/$',
     DetailView.as_view(model=Event,
                        context_object_name='content',)),

    # Bruker
    (r'^mine$', 'show_user'),
    (r'^(?P<event_id>\d{1,8})/registrering$', 'register_user'),

    # Eksporter
    (r'^(?P<event_id>\d{1,8})/eksporter$', 'ical_event'),
)

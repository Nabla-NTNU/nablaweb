# arrangement/urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('arrangement.views',
# Administrasjon
    (r'^opprett/$', 'create_or_edit_event'),
    (r'^(?P<event_id>\d{1,8})/admin$', 'administer'),
    (r'^(?P<event_id>\d{1,8})/endre$', 'create_or_edit_event'),
    (r'^(?P<event_id>\d{1,8})/slett$', 'delete'),
# Offentlig
    (r'^$', 'list_events'),
    (r'^(?P<event_id>\d{1,8})/$', 'show_event'),
# Bruker
    (r'^mine$', 'show_user'),
    (r'^(?P<event_id>\d{1,8})/registrering$', 'register_user'),
# Eksporter
    (r'^(?P<event_id>\d{1,8})/eksporter$', 'ical_event'),
)

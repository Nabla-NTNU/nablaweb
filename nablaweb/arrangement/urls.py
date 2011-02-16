# arrangement/urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('arrangement.views',
# Administrasjon
    (r'^create/$', 'create'),
    (r'^(?P<event_id>\d+)/status$', 'status'),
    (r'^(?P<event_id>\d+)/edit$', 'edit'),
    (r'^(?P<event_id>\d+)/delete$', 'confirm_deletion'),
    (r'^(?P<event_id>\d+)/delete_event$', 'delete'),
# Offentlig
    (r'^$', 'overview'),
    (r'^(?P<event_id>\d+)/$', 'details'),
# Bruker
    (r'^my_events/$', 'show_user'),
    (r'^(?P<event_id>\d+)/registration$', 'registration'),
    (r'^(?P<event_id>\d+)/register$', 'register'),
# Eksporter
    (r'^(?P<event_id>\d+)/ical$', 'ical_event'),
    (r'^(?P<event_id>\d+)/my_events/ical$', 'ical_user'),
)

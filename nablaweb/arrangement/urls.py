# arrangement/urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('arrangement.views',
# Administrasjon
    (r'^opprett/$', 'opprett'),
    (r'^(?P<arr_id>\d+)/status$', 'status'),
    (r'^(?P<arr_id>\d+)/endre$', 'endre'),
    (r'^(?P<arr_id>\d+)/slett$', 'bekreft_sletting'),
    (r'^(?P<arr_id>\d+)/slett_arrangement$', 'slett'),
# Offentlig
    (r'^$', 'oversikt'),
    (r'^(?P<arr_id>\d+)/$', 'detaljer'),
# Bruker
    (r'^mine/$', 'vis_bruker'),
    (r'^(?P<arr_id>\d+)/paamelding$', 'meld_paa'),
# Eksporter
    (r'^(?P<arr_id>\d+)/ical$', 'ical_arrangement'),
    (r'^(?P<arr_id>\d+)/mine/ical$', 'ical_bruker'),
)

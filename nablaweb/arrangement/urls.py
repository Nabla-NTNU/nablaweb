# arrangement/urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('arrangement.views',
# Administrasjon
    (r'^opprett/$', 'opprett'),
    (r'^(?P<arrangement_id>)\d+/status$', 'status'),
    (r'^(?P<arrangement_id>)\d+/endre$', 'endre'),
    (r'^(?P<arrangement_id>)\d+/slett$', 'bekreft_sletting'),
    (r'^(?P<arrangement_id>)\d+/slett_arrangement$', 'slett'),
# Offentlig
    (r'^$', 'oversikt'),
    (r'^(?P<arrangement_id>)\d+/$', 'detaljer'),
# Bruker
    (r'^mine/$', 'vis_bruker'),
    (r'^(?P<arrangement_id>)\d+/paamelding$', 'meld_paa'),
# Eksporter
    (r'^(?P<arrangement_id>)\d+/vcal$', 'vcal_arrangement'),
    (r'^(?P<arrangement_id>)\d+/mine/eskporter$', 'vcal_bruker'),
)

# -*- coding: utf-8 -*-
from content.models import Event
from bedpres.models import BedPres
from datetime import datetime
from itertools import chain
from operator import attrgetter


def get_primary_dir(request):
    """Adds the primary URL path to context.

    For example, if the user is visting http://nabla.no/batman/cakes,
    primary_dir would be "batman".

    """
    primary_dir = request.path.split('/')[1]
    if primary_dir:
        primary_dir_slashes = '/' + primary_dir + '/'
    else:
        primary_dir_slashes = '/'
    return {'primary_dir': primary_dir,
            'primary_dir_slashes': primary_dir_slashes}


def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events"""
    # Henter alle events som startet for 6 timer siden og senere
    now = datetime.now() - timedelta(hours=6)
    upcoming_events = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming_bedpresses = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming = sorted(chain(upcoming_events, upcoming_bedpresses), key=attrgetter("event_start"))[:6]
    return {'upcoming_events': upcoming}

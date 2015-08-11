# -*- coding: utf-8 -*-

from datetime import datetime
from itertools import chain
from operator import attrgetter

from content.models.events import Event


def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events"""
    now = datetime.now()
    upcoming_events = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    # upcoming_bedpresses = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming = sorted(chain(upcoming_events), key=attrgetter("event_start"))[:6]
    return {'upcoming_events': upcoming}

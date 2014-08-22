# -*- coding: utf-8 -*-

from events.models import Event
from bedpres.models import BedPres
from datetime import datetime
from itertools import chain

def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events, og upcoming_bedpresses"""
    now = datetime.now()
    upcoming_events = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming_bedpresses = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming = sorted(chain(upcoming_events,upcoming_bedpresses),cmp=lambda e1,e2: 1 if e1.event_start>e2.event_start else  -1)[:6]
    return {'upcoming_events': upcoming, 'upcoming_bedpresses': upcoming_bedpresses}

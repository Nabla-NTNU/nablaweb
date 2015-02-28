# -*- coding: utf-8 -*-

from .models import Event
from bedpres.models import BedPres
from datetime import datetime
from itertools import chain
from operator import attrgetter


def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events, og upcoming_bedpresses"""
    now = datetime.now()
    upcoming_events = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming_bedpresses = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming = sorted(chain(upcoming_events, upcoming_bedpresses), key=attrgetter("event_start"))[:6]
    return {'upcoming_events': upcoming,
            'upcoming_bedpresses': upcoming_bedpresses}

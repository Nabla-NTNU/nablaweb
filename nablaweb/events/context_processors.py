# -*- coding: utf-8 -*-

from events.models import Event

def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events"""

    # TODO: Denne må filtreres slik at den ikke viser eldre events
    upcoming_events = Event.objects.all()[:5]

    return {'upcoming_events': upcoming_events}

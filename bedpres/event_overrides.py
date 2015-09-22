from bedpres.models import BedPres
from content.models import Event

from content.views.events import set_current_events, set_get_event
from itertools import chain
from django.shortcuts import get_object_or_404


def get_current_events(year, month):
    # Get this months events and bedpreser separately
    events = Event.objects.select_related("content_type").filter(
        event_start__year=year,
        event_start__month=month)
    bedpress = BedPres.objects.select_related("content_type").filter(
        event_start__year=year,
        event_start__month=month)

    # Combine them to a single calendar
    return chain(events, bedpress)

set_current_events(get_current_events, True)


def get_event(event_id):
    # Try Event first, then BedPres. 404 if none of them are found.
    try:
        return Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return get_object_or_404(BedPres, pk=event_id)


set_get_event(get_event, True)

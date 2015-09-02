from bedpres.models import BedPres
from content.models import Event

from content.views.events import set_current_events
from itertools import chain


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
"""
This is a hack
"""
from datetime import datetime, time
from itertools import chain
from bpc_client.event import get_events as get_bpc_events

from nablapps.events.event_overrides import EventGetter
from nablapps.events.models import Event
from .models import BedPres


class BedPresAndEventGetter(EventGetter):
    """
    Class without instance variables
    """

    @staticmethod
    def get_current_events(year, month):
        # Get this months events and bedpreser separately
        events = Event.objects.filter(
            event_start__year=year,
            event_start__month=month) |\
            Event.objects.filter(
                event_end__year=year,
                event_end__month=month)
        bedpress = BedPres.objects.filter(
            event_start__year=year,
            event_start__month=month)

        # Combine them to a single calendar
        return chain(events, bedpress)

    @staticmethod
    def attending_events(user, today):
        if user.is_anonymous:
            return []
        events = EventGetter.attending_events(user, today)
        bpc_events = get_bpc_events(
            username=user.username,
            fromdate=datetime.combine(today, time())
        )
        bpcids = [e.id for e in bpc_events]
        bedpresses = BedPres.objects.filter(bpcid__in=bpcids)
        return list(events) + list(bedpresses)

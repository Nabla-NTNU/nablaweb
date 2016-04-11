from datetime import datetime, time
from bedpres.models import BedPres
from content.models import Event

from bpc_client.event import get_events as get_bpc_events

from content.event_overrides import EventGetter
from itertools import chain
from django.shortcuts import get_object_or_404


class BedPresAndEventGetter(EventGetter):

    @staticmethod
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

    @staticmethod
    def get_event(event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return get_object_or_404(BedPres, pk=event_id)

    @staticmethod
    def attending_events(user, today):
        if user.is_anonymous():
            return []
        events = EventGetter.attending_events(user, today)
        bpc_events = get_bpc_events(username=user.username, fromdate=datetime.combine(today, time()))
        bpcids = [e.id for e in bpc_events]
        bedpresses = BedPres.objects.filter(bpcid__in=bpcids)
        return list(events) + list(bedpresses)

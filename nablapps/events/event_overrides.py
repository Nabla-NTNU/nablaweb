"""
A dirty legacy hack for getting events and bedpres objects together.

See event_overrides.py in bedpres

It was needed at the time events was in the content-app repo,
but might not be needed anymore.
"""
import importlib
from django.conf import settings

from .models import Event


class EventGetter:
    """
    Default implementation of EventGetter. Gets only Event objects.
    """
    @staticmethod
    def get_current_events(year, month):
        """Get events this month and year"""
        return Event.objects.filter(
            event_start__year=year,
            event_start__month=month)

    @staticmethod
    def attending_events(user, today):
        """Get the future events attended by a user"""
        if user.is_anonymous():
            return []
        regs = user.eventregistration_set.filter(event__event_start__gte=today)
        events = []
        for reg in regs:
            event = reg.event
            event.attending = reg.attending
            event.waiting = not reg.attending
            events.append(event)
        return events


def get_eventgetter():
    """
    Get the current eventgetter class from settings.
    Use default EventGetter if not found in settings.
    """
    try:
        class_path = settings.EVENT_GETTER_CLASS
    except AttributeError:
        return EventGetter
    module_path, _, class_name = class_path.rpartition('.')
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

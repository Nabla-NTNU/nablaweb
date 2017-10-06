from django.conf import settings
import importlib

from .models import Event


class EventGetter(object):
    @staticmethod
    def get_current_events(year, month):
        return Event.objects.filter(
            event_start__year=year,
            event_start__month=month)

    @staticmethod
    def get_event(event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return None

    @staticmethod
    def attending_events(user, today):
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
    try:
        class_path = settings.EVENT_GETTER_CLASS
    except AttributeError:
        return EventGetter
    module_path, _, class_name = class_path.rpartition('.')
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

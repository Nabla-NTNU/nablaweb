from django.conf import settings
import importlib

from content.models import Event


class EventGetter(object):
    @staticmethod
    def get_current_events(year, month):
        return Event.objects.select_related("content_type").filter(
            event_start__year=year,
            event_start__month=month)

    @staticmethod
    def get_event(event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return None


def get_eventgetter():
    try:
        class_path = settings.EVENT_GETTER_CLASS
    except AttributeError:
        return EventGetter
    module_path, _, class_name = class_path.rpartition('.')
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


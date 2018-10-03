"""
Tests for the EventGetter hack
"""
# pylint: disable=C0111,C0301
from datetime import datetime, timedelta
from django.test import TestCase, override_settings
from django.conf import settings

from nablapps.events.models import Event
from nablapps.events.event_overrides import EventGetter, get_eventgetter

from .event_override_test_dummy_module import TestGetter


class EventGetterTest(TestCase):

    def test_get_current_events(self):
        some_year = 2016
        some_month = 4
        event_start = [datetime(year=some_year, month=some_month, day=i) for i in range(1, 21)]
        event_end = [a + timedelta(hours=2) for a in event_start]
        events_in_month = [
            Event.objects.create(headline="event %s" % i, event_start=a, event_end=b)
            for i, (a, b) in enumerate(zip(event_start, event_end))
        ]
        self.assertCountEqual(
            EventGetter.get_current_events(some_year, some_month),
            events_in_month
        )


class GetEventGetterTest(TestCase):

    @override_settings()
    def test_no_event_override_setting(self):
        del settings.EVENT_GETTER_CLASS
        self.assertIs(get_eventgetter(), EventGetter)

    @override_settings(EVENT_GETTER_CLASS='nablapps.events.event_overrides.EventGetter')
    def test_with_event_override_setting(self):
        self.assertIs(get_eventgetter(), EventGetter)

    @override_settings(EVENT_GETTER_CLASS='nablapps.events.tests.event_override_test_dummy_module.TestGetter')
    def test_with_event_override_setting_dummy(self):
        self.assertIs(get_eventgetter(), TestGetter)

    @override_settings(EVENT_GETTER_CLASS='some.nonexisting.module.MyClass')
    def test_unknown_module(self):
        self.assertRaises(ImportError, get_eventgetter)

    @override_settings(EVENT_GETTER_CLASS='nablapps.events.tests.event_override_test_dummy_module.NonExistantClass')
    def test_unknown_class(self):
        self.assertRaises(AttributeError, get_eventgetter)

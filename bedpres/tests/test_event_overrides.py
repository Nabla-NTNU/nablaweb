from datetime import datetime, timedelta

from content.models.events import Event
from django.test import TestCase

from bedpres.event_overrides import BedPresAndEventGetter
from bedpres.models import BedPres
from nablapps.jobs.models import Company


class EventGetterTest(TestCase):

    def test_get_event(self):
        event = Event.objects.create()
        company = Company.objects.create()
        bedpres = BedPres.objects.create(company=company)
        self.assertEqual(BedPresAndEventGetter.get_event(event.id), event)
        self.assertEqual(BedPresAndEventGetter.get_event(bedpres.id), bedpres)

    def test_get_current_events(self):
        some_year = 2016
        some_month = 4
        event_start = [datetime(year=some_year, month=some_month, day=i) for i in range(1, 21)]
        event_end = [a + timedelta(hours=2) for a in event_start]
        events_in_month = [
            Event.objects.create(headline="event %s" % i, event_start=a, event_end=b)
            for i, (a, b) in enumerate(zip(event_start, event_end))
            ]
        bedpres_in_month = [
            Event.objects.create(headline="event %s" % i, event_start=a, event_end=b)
            for i, (a, b) in enumerate(zip(event_start, event_end))
            ]
        self.assertCountEqual(
            BedPresAndEventGetter.get_current_events(some_year, some_month),
            events_in_month + bedpres_in_month
        )

from datetime import datetime, timedelta

from nablapps.events.models import Event
from django.test import TestCase

from nablapps.bedpres.event_overrides import BedPresAndEventGetter
from nablapps.bedpres.models import BedPres
from nablapps.jobs.models import Company


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
        bedpres_in_month = [
            BedPres.objects.create(headline="event %s" % i, event_start=a, event_end=b,
                                   company=Company.objects.get_or_create()[0],
                                   bpcid=i)
            for i, (a, b) in enumerate(zip(event_start, event_end))
            ]
        self.assertCountEqual(
            BedPresAndEventGetter.get_current_events(some_year, some_month),
            events_in_month + bedpres_in_month
        )

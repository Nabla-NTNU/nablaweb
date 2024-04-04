"""
Tests things that has to do with time and deadlines
"""

# pylint: disable=C0111
from datetime import datetime, timedelta

from .common import GeneralEventTest


class TimeTest(GeneralEventTest):
    def _test_time_has_passed(self, field, method):
        now = datetime.now()
        an_hour = timedelta(hours=1)

        test_method = getattr(self.event, method)

        setattr(self.event, field, now - an_hour)
        self.event.save()
        self.assertTrue(test_method())

        setattr(self.event, field, now + an_hour)
        self.event.save()
        self.assertFalse(test_method())

    def test_has_started(self):
        self._test_time_has_passed("event_start", "has_started")

    def test_has_finished(self):
        self._test_time_has_passed("event_end", "has_finished")

        self.event.event_end = None
        self.event.save()
        self.assertFalse(self.event.has_finished())

    def test_registration_has_started(self):
        self._test_time_has_passed("registration_start", "registration_has_started")

    def test_registration_open(self):
        now = datetime.now()
        an_hour = timedelta(hours=1)

        times = ((-2, -1, False), (-1, 1, True), (1, 2, False))

        for a, b, is_open in times:
            self.event.registration_start = now + a * an_hour
            self.event.registration_deadline = now + b * an_hour
            self.event.save()
            self.assertEqual(self.event.registration_open(), is_open, msg=f"{a},{b}")

    def test_registration_open_when_not_registration_required(self):
        self.event.registration_required = False
        self.event.registration_deadline = datetime.now() - timedelta(hours=1)
        self.event.save()
        self.event.registration_open()

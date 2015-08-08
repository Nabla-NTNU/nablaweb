from datetime import datetime

from django.test import TestCase

from content.models.events import Event
from content.templatetags.event_extras import google_calendarize


class GoogleCalendarizeTestCase(TestCase):

    def test_google_calendarize(self):
        event = Event.objects.create(
            location="Here",
            headline="Title",
            event_start=datetime(2030, 1, 1),
        )
        url = google_calendarize(event)

        self.assertIn(event.headline, url)
        self.assertIn(event.location, url)

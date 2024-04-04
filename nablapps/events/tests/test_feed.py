"""
Test the event rss feed
"""

# pylint: disable=C0111,C0301
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from nablapps.events.models import Event


@override_settings(ROOT_URLCONF="nablapps.events.urls")
class RecentEventsTestCase(TestCase):
    def test_feed(self):
        events = [
            Event.objects.create(headline=f"Event{i}", lead_paragraph=f"Yo{i}")
            for i in range(10)
        ]
        c = Client()
        response = c.get(reverse("event_feed"))
        for event in events:
            self.assertContains(response, event.headline)
            self.assertContains(response, event.lead_paragraph)

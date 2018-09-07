from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse

from nablapps.events.models import Event


@override_settings(ROOT_URLCONF="nablapps.events.urls")
class RecentEventsTestCase(TestCase):

    def test_feed(self):
        events = [Event.objects.create(headline=f"Event{i}", lead_paragraph=f"Yo{i}") for i in range(10)]
        c = Client()
        response = c.get(reverse("event_feed"))
        for event in events:
            self.assertContains(response, event.headline)
            self.assertContains(response, event.lead_paragraph)

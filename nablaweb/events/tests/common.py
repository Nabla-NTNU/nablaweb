
from django.test import TestCase
from datetime import datetime

from accounts.models import NablaUser as User
from events.models import Event


class GeneralEventTest(TestCase):
    def setUp(self):
        # Lag en bruker som kan "lage" arrangementet
        self.user = User.objects.create(username='oyvinlek',
                                        password='oyvinlek')

        # Opprett et arrangement
        self.event = Event.objects.create(
            created_by=self.user,
            location="Here",
            headline="Title",
            lead_paragraph="Text.",
            body="More text.",
            event_start=datetime(2030, 1, 1),
            registration_deadline=datetime(2029, 1, 1),
            registration_start=datetime(2000, 1, 1),
            registration_required=True,
            places=10,
            has_queue=True,
            )

        self.users = [
            User.objects.create(
                username="user%d" % i,
                password="user%d" % i,
                email="user%d@localhost" % i)
            for i in range(1, 10)
        ]

"""
This module contains things that are in common
for the different event tests.
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from nablapps.events.models import Event

User = get_user_model()


class GeneralEventTest(TestCase):
    """
    Sets up some events and users to be used in other tests.
    """

    def setUp(self):
        # Lag en bruker som kan "lage" arrangementet
        self.user = User.objects.create(
            username="admin", password="admin", email="admin@localhost"
        )

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
                username=f"user{i}", password=f"user{i}", email=f"user{i}@localhost"
            )
            for i in range(1, 10)
        ]

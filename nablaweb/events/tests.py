# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta

from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model; User = get_user_model()

from events.models import Event, EventException
from events.exceptions import RegistrationAlreadyExists


class GeneralEventTest(TestCase):
    def setUp(self):
        # Lag en bruker som kan "lage" arrangementet
        self.user = User.objects.create(username='oyvinlek', password='oyvinlek')

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


class RegistrationTest(GeneralEventTest):

    def test_register_and_deregister(self):
        self.event.register_user(self.user)
        self.assertTrue(self.event.is_registered(self.user))

        self.event.deregister_user(self.user)
        self.assertFalse(self.event.is_registered(self.user))

    def test_register_if_already_registered(self):
        self.event.register_user(self.user)
        self.assertTrue(self.event.is_registered(self.user))
        self.assertRaises(RegistrationAlreadyExists, self.event.register_user, self.user)

    def test_raises_exception_on_registration_required_false(self):
        self.event.registration_required = False
        self.event.save()
        self.assertRaises(EventException, self.event.register_user, self.user)

    def test_registration_closed(self):
        self.event.registration_deadline = datetime(1940, 1, 1)
        self.event.save()
        self.assertRaises(EventException, self.event.register_user, self.user)

    def test_event_full(self):
        u = User.objects.create(username="anotheruser")
        u.save()
        self.event.places = 1
        self.event.has_queue = False
        self.event.save()
        self.event.register_user(u)
        self.assertRaises(EventException, self.event.register_user, self.user)

    def test_deregistration_closed(self):
        self.event.deregistration_deadline = datetime(1940, 1, 1)
        self.event.save()
        self.event.register_user(self.user)
        self.assertRaises(EventException, self.event.deregister_user, self.user)


class WaitingListTest(GeneralEventTest):
    def setUp(self):
        super(WaitingListTest, self).setUp()

        # Lag og registrer noen brukere
        self.event.register_user(self.user)
        for i in range(1, 20):
            u = User.objects.create(username='user%d'%i, password='user%d'%i, email='user%d@localhost'%i)
            self.event.register_user(u)

    def test_attending_ordering(self):
        attending = self.event.attending_registrations
        for i, reg in enumerate(attending, start=1):
            self.assertEqual(reg.number, i)

    def test_waiting_ordering(self):
        waiting = self.event.waiting_registrations
        for i, reg in enumerate(waiting, start=1):
            self.assertEqual(reg.number, i)

    def test_deregister_user(self):
        while self.event.eventregistration_set.all():
            reg = random.choice(self.event.eventregistration_set.all())
            user = reg.user
            self.event.deregister_user(user)
            self.test_attending_ordering()
            self.test_waiting_ordering()

    def test_set_attending_and_send_email(self):
        # Finner førstemann på ventelista
        waiting_reg = self.event.registrations_manager.first_on_waiting_list()
        u = waiting_reg.user

        self.assertFalse(self.event.is_attending(u))
        waiting_reg.set_attending_and_send_email()

        # Skjekk om det ble sendt epost
        self.assertTrue(self.event.is_attending(u))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], u.email)


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
            self.event.registration_start = now + a*an_hour
            self.event.registration_deadline = now + b*an_hour
            self.event.save()
            self.assertEqual(self.event.registration_open(), is_open, msg="{a},{b}".format(**locals()))

    def test_registration_open_when_not_registration_required(self):
        self.event.regstration_required = False
        self.event.registration_deadline = datetime.now() - timedelta(hours=1)
        self.event.registration_open()

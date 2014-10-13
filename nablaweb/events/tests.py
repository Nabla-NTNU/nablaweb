# -*- coding: utf-8 -*-
import unittest
import datetime
import random

from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model; User = get_user_model()

from events.models import Event, EventRegistration, RegistrationException


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
            event_start=datetime.datetime(2030,1,1),
            registration_deadline=datetime.datetime(2029,1,1),
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

    def test_raises_exception_on_registration_required_false(self):
        self.event.registration_required = False
        self.event.save()
        self.assertRaises(RegistrationException, self.event.register_user, self.user)

    def test_registration_closed(self):
        self.event.registration_deadline = datetime.datetime(1940, 1, 1)
        self.event.save()
        self.assertRaises(RegistrationException, self.event.register_user, self.user)

    def test_event_full(self):
        u = User.objects.create(username="anotheruser")
        u.save()
        self.event.places = 1
        self.event.has_queue = False
        self.event.save()
        self.event.register_user(u)
        self.assertRaises(RegistrationException, self.event.register_user, self.user)

    def test_deregistration_closed(self):
        self.event.deregistration_deadline = datetime.datetime(1940, 1, 1)
        self.event.save()
        self.event.register_user(self.user)
        self.assertRaises(RegistrationException, self.event.deregister_user, self.user)


class WaitingListTest(GeneralEventTest):
    def setUp(self):
        super(WaitingListTest, self).setUp()

        # Lag og registrer noen brukere
        self.event.register_user(self.user)
        for i in xrange(1, 20):
            u = User.objects.create(username='user%d'%i, password='user%d'%i, email='user%d@localhost'%i)
            self.event.register_user(u)

    def test_ordering(self):
        attending = self.event.eventregistration_set.filter(attending=True).order_by('number')
        for i, reg in enumerate(attending, start=1):
            self.assertEqual(reg.number, i)

        waiting = self.event.eventregistration_set.filter(attending=False).order_by('number')
        for i, reg in enumerate(waiting, start=1):
            self.assertEqual(reg.number, i)

    def test_deregister_user(self):
        while self.event.users_registered() != 0:
            reg = random.choice(self.event.eventregistration_set.all())
            user = reg.user
            self.event.deregister_user(user)
            self.test_ordering()

    def test_set_attending(self):
        # Finner førstemann på ventelista
        waiting_reg = self.event.registrations_manager.first_on_waiting_list()
        u = waiting_reg.user

        self.assertFalse(self.event.is_attending(u))
        waiting_reg.set_attending()

        # Skjekk om det ble sendt epost
        self.assertTrue(self.event.is_attending(u))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], u.email)



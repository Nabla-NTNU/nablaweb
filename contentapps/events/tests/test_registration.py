# -*- coding: utf-8 -*-

import random
from datetime import datetime

from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()

from contentapps.events.exceptions import RegistrationAlreadyExists, EventException

from .common import GeneralEventTest


class RegistrationTest(GeneralEventTest):

    def test_register_and_deregister(self):
        self.event.register_user(self.user)
        self.assertTrue(self.event.is_registered(self.user))

        for user in self.users:
            self.event.register_user(user)
            self.assertTrue(self.event.is_registered(user))

        self.event.deregister_user(self.user)
        self.assertFalse(self.event.is_registered(self.user))

        for user in self.users:
            self.event.deregister_user(user)
            self.assertFalse(self.event.is_registered(user))

    def test_email_list(self):
        for user in self.users:
            self.event.register_user(user)

        emails = self.event.users_attending_emails()

        for user in self.users:
            self.assertIn(user.email, emails)

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
        for u in self.users:
            self.event.register_user(u)

        registered = len(self.users) + 1
        for i in range(registered, 2*self.event.places):
            u = User.objects.create(
                username="user%d" % i,
                password="user%d" % i,
                email="user%d@localhost" % i)
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

    def test_add_places(self):
        w_0 = self.event.users_waiting()
        u = self.event.waiting_registrations[5].user
        self.event.places += 5
        self.event.save()
        self.assertTrue(self.event.is_full())
        self.assertEqual(w_0 - 5, self.event.users_waiting())
        self.assertEqual(u, self.event.registrations_manager.first_on_waiting_list().user)

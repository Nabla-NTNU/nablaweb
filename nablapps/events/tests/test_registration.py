"""
Tests for registration to an event
"""
# pylint: disable=C0111,C0301
import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.exceptions import ValidationError

from nablapps.events.exceptions import EventException, RegistrationAlreadyExists

from .common import GeneralEventTest

User = get_user_model()


class RegistrationTest(GeneralEventTest):
    """
    Tests for registration
    """

    def test_non_registered_users_are_not_registered(self):
        for user in self.users:
            self.assertFalse(self.event.is_registered(user))

    def test_register_and_deregister(self):

        for user in self.users:
            self.event.register_user(user)
            self.assertTrue(self.event.is_registered(user))

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
        self.assertRaises(
            RegistrationAlreadyExists, self.event.register_user, self.user
        )

    def test_raises_exception_on_registration_required_false(self):
        self.event.registration_required = False
        self.event.save()
        self.assertRaises(EventException, self.event.register_user, self.user)

    def test_registration_closed(self):
        self.event.registration_deadline = datetime(1940, 1, 1)
        self.event.save()
        self.assertRaises(EventException, self.event.register_user, self.user)

    def test_event_full(self):
        self.event.places = 1
        self.event.has_queue = False
        self.event.save()
        self.event.register_user(self.users[0])
        self.assertRaises(EventException, self.event.register_user, self.user)

    def test_deregistration_closed(self):
        self.event.deregistration_deadline = datetime(1940, 1, 1)
        self.event.save()
        self.event.register_user(self.user)
        self.assertRaises(EventException, self.event.deregister_user, self.user)


class PenaltyTest(GeneralEventTest):
    """Tests for the penalty system"""

    def test_invalid_penalty_rule(self):
        """Tries setting the penalty rule of event to invalid value"""
        self.event.penalty = -1
        self.assertRaises(ValidationError, self.event.clean_fields)

    def test_penalty_none_on_registration_required(self):
        """Setting penalty rule to None when registration is required"""
        self.event.penalty = None
        self.event.registration_required = True
        self.assertRaises(ValidationError, self.event.clean)

    def test_setting_invalid_penalty_value_in_registration(self):
        """Tries setting penalty in registration request to some thing not valid for the event"""
        self.event.register_user(self.user)
        event_reg = self.event.eventregistration_set.first()
        event_reg.penalty = -1  # Invalid penalty
        self.assertRaises(ValidationError, event_reg.clean)


class WaitingListTest(GeneralEventTest):
    """
    Tests everything concerning the waiting list
    """

    def setUp(self):
        super().setUp()

        # Lag og registrer noen brukere
        self.event.register_user(self.user)
        for u in self.users:
            self.event.register_user(u)

        registered = len(self.users) + 1
        for i in range(registered, 2 * self.event.places):
            u = User.objects.create(
                username=f"user{i}", password=f"user{i}", email=f"user{i}@localhost"
            )
            self.event.register_user(u)

    def test_deregister_user(self):
        while self.event.eventregistration_set.all():
            reg = random.choice(self.event.eventregistration_set.all())
            user = reg.user
            self.event.deregister_user(user)

    def test_set_attending_and_send_email(self):
        # Finner førstemann på ventelista
        waiting_reg = self.event.waiting_registrations[0]
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
        self.assertEqual(u, self.event.waiting_registrations[0].user)


class WaitingListTest2(GeneralEventTest):
    def test_correct_order_from_waiting_list(self):
        self.event.places = 5
        self.event.save()

        registrations = [self.event.register_user(user) for user in self.users]

        self.assertTrue(self.event.is_attending(self.users[0]))
        self.assertTrue(self.event.is_waiting(self.users[5]))
        self.assertFalse(self.event.is_attending(self.users[5]))
        self.assertEqual(registrations[5].waiting_list_place(), 1)

        self.event.deregister_user(self.users[0])
        self.assertTrue(self.event.is_attending(self.users[5]))

        self.event.deregister_user(self.users[6])
        self.event.deregister_user(self.users[2])
        self.assertTrue(self.event.is_attending(self.users[7]))

        self.event.deregister_user(self.users[4])
        self.assertTrue(self.event.is_attending(self.users[8]))

        self.event.deregister_user(self.users[1])

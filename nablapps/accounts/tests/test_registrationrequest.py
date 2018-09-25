from django.core import mail
from django.urls import reverse
from django.test import TestCase, Client

from nablapps.accounts.models import NablaUser, RegistrationRequest


class BaseRegistrationTest(TestCase):
    def setUp(self):
        self.username = "someusername"
        self.first_name = "Ola"
        self.last_name = "Nordmann"
        self.data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


class RegistrationViewTest(BaseRegistrationTest):

    def test_create_registration_request(self):
        client = Client()
        client.post(
            reverse("user_registration"),
            data=self.data
        )
        reg = RegistrationRequest.objects.get(username=self.username)
        self.assertEqual(reg.first_name, self.first_name)
        self.assertEqual(reg.last_name, self.last_name)

    def create_inactive_user(self):
        user = NablaUser.objects.create(**self.data)
        user.is_active = False
        user.save()

    def test_create_user(self):
        self.create_inactive_user()

        client = Client()
        client.post(
            reverse("user_registration"),
            data=self.data
        )
        user = NablaUser.objects.get(username=self.username)
        self.assertTrue(user.is_active, msg="The user should be active.")
        self.assertEqual(
            mail.outbox[0].to[0], user.email,
            msg="There should have been sent an email to the new user.")

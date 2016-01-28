from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail

from accounts.forms import RegistrationForm
from accounts.models import NablaUser, RegistrationRequest


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


class RegistrationFormTest(BaseRegistrationTest):
    def setUp(self):
        super().setUp()
        self.form = RegistrationForm(self.data)

    def test_valid_new_user(self):
        NablaUser.objects.create(username=self.username, is_active=False)
        self.assertTrue(self.form.is_valid())

    def test_user_not_in_database(self):
        self.assertFalse(self.form.is_valid())

    def test_user_already_activated(self):
        NablaUser.objects.create(username=self.username, is_active=True)
        self.assertFalse(self.form.is_valid())

    def test_create_registration_request(self):
        self.form.is_valid()

        reg = RegistrationRequest.objects.get(username=self.username)
        self.assertEqual(reg.first_name, self.first_name)
        self.assertEqual(reg.last_name, self.last_name)


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
        self.assertEqual(mail.outbox[0].to[0], user.email,
            msg="There should have been sent an email to the new user.")

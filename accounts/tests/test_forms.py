from django.test import TestCase

from accounts.forms import RegistrationForm
from accounts.models import NablaUser


class RegistrationFormTest(TestCase):
    def setUp(self):
        self.username = "someusername"
        self.form = RegistrationForm({
            "username": self.username,
            "first_name": "Ola",
            "last_name": "Nordmann"
        })

    def test_valid_new_user(self):
        NablaUser.objects.create(username=self.username, is_active=False)
        self.assertTrue(self.form.is_valid())

    def test_user_not_in_database(self):
        self.assertFalse(self.form.is_valid())

    def test_user_already_activated(self):
        NablaUser.objects.create(username=self.username, is_active=True)
        self.assertFalse(self.form.is_valid())

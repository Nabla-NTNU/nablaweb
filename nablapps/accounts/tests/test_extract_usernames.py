from django.test import TestCase

from nablapps.accounts.models import NablaUser
from nablapps.accounts.utils import extract_usernames


class TestExtractUsername(TestCase):
    def test_extract_usernames(self):
        s = "brukernavn@stud.ntnu.no\nannetbrukernavn@stud.ntnu.no"
        extract_usernames(s)
        self.assertTrue(NablaUser.objects.filter(username="brukernavn").exists())
        self.assertTrue(NablaUser.objects.filter(username="annetbrukernavn").exists())
        self.assertFalse(NablaUser.objects.filter(username="lalaland").exists())

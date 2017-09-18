from django.test import TestCase

from accounts.models import NablaUser, FysmatClass
from nablapps.bedpres.utils import get_bpc_user_dictionary, InvalidCardNum


class BpcUserDictionaryTest(TestCase):

    def setUp(self):
        self.user = NablaUser.objects.create(
            username="hei",
            first_name="Scooby",
            last_name="Doo",
            ntnu_card_number="1234567890"
        )
        c = FysmatClass.objects.create(starting_year=2012)
        c.user_set.add(self.user)

    def assert_bpc_dict_contains_all(self, dict):
        self.assertEqual(dict.keys(), {"fullname", "username", "card_no", "year"})

    def test_valid_user(self):
        bpc_dict = get_bpc_user_dictionary(self.user)
        self.assert_bpc_dict_contains_all(bpc_dict)

    def test_invalid_cardnumber(self):
        self.user.ntnu_card_number = "invalid"
        self.user.save()

        with self.assertRaises(InvalidCardNum):
            get_bpc_user_dictionary(self.user)
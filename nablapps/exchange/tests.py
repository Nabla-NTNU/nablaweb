from django.test import TestCase
from datetime import datetime

from nablapps.accounts.models import NablaUser
from nablapps.exchange.models import University, Exchange, RETNINGER


class TestUniversityGetRetningList(TestCase):
    def setUp(self):
        self.student = NablaUser.objects.create(username="thexchanger")
        self.univ = University.objects.create(
            univ_navn="YOLO",
            land="Der ingen skulle tru at nokon kunne bu."
        )

    def test_no_exchanges(self):
        l = self.univ.get_has_retning_list()
        self.assertFalse(any(l))

    def test_length_equal_to_retning_choice_list(self):
        l = self.univ.get_has_retning_list()
        self.assertEqual(len(l), len(RETNINGER))

    def test_one_retning(self):
        number = 0
        Exchange.objects.create(
            student=self.student,
            univ=self.univ,
            retning=RETNINGER[number][0],
            start=datetime.now(),
            end=datetime.now()
        )
        l = self.univ.get_has_retning_list()
        self.assertTrue(l[number])

"""
Tests related to bedpres
"""


from django.core.exceptions import ValidationError
from .common import GeneralEventTest
from nablapps.jobs.models import Company

class BedpresTest(GeneralEventTest):
    def test_company_not_set_bedpres(self):
        self.event.is_bedpres=True
        self.event.company=None
        self.assertRaises(ValidationError, self.event.clean)

    def test_company_set_when_not_bedpres(self):
        self.event.is_bedpres=False
        self.event.company=Company.objects.create(name="Some company")
        self.assertRaises(ValidationError, self.event.clean)

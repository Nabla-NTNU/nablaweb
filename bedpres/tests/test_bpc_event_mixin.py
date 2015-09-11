from django.test import TestCase
from bedpres.bpcmixin import BedpresNoModel


bpc_event_data = {
    "count_waiting": 0,
    "deadline": "2019-10-11 17:00:00",
    "deadline_passed": "0",
    "description": "Dette er en kjempebra bedrift.",
    "description_formatted": "<p>Dette er en kjempebra bedrift.</p>\n",
    "id": "10",
    "is_advertised": "1",
    "max_year": "3",
    "min_year": "3",
    "open_for": "3",
    "place": "kontoret",
    "registration_start": "2019-10-11 11:00:00",
    "registration_started": "0",
    "seats": "10",
    "seats_available": "10",
    "this_attending": "0",
    "time": "2023-10-12 17:00:00",
    "title": "jesus",
    "waitlist_enabled": "1",
    "web_page": "http://jesus.com"
}


class BPCTestCase(TestCase):

    def test_create(self):
        BedpresNoModel(100)

    def test_get_event_data(self):
        b = BedpresNoModel(100)
        b.bpc_event.data = bpc_event_data
        self.assertIsInstance(b.bpc_event.registration_started, bool)

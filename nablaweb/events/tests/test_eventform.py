
from collections import ChainMap
from django.test import TestCase

from events.forms import EventForm


class EventFormTestCase(TestCase):

    def assertFormValid(self, form):
        self.assertTrue(form.is_valid(), "Form should be valid but has these errors: {}".format(form.errors))

    def assertFormInValid(self, form):
        self.assertFalse(form.is_valid(), "Form should be invalid but isn't")

    def get_smallest_valid_form(self):
        return {
            "headline": "Headline",
            "event_start_0": "2015-10-01",
            "event_start_1": "08:00",
            "priority": "5",
            "location": "Here"
        }

    def get_valid_registration_form_dict(self):
        return ChainMap({
            "registration_required": "1",
            "places": "20",
            "registration_deadline_0": "2015-09-01",
            "registration_deadline_1": "08:00",
            "has_queue": "0"
        }, self.get_smallest_valid_form())

    def test_empty_form(self):
        self.assertFormInValid(EventForm({}))

    def test_smallest_valid_form(self):
        self.assertFormValid(EventForm(self.get_smallest_valid_form()))

    def test_event_end_before_event_start(self):
        form_dict = self.get_smallest_valid_form()
        form_dict["event_end_0"] = form_dict["event_start_0"]
        form_dict["event_end_1"] = "07:00"
        self.assertFormInValid(EventForm(form_dict))

    def test_with_registration_without_required_info(self):
        form_dict = self.get_smallest_valid_form()
        form_dict["registration_required"] = "1"
        form = EventForm(form_dict)
        self.assertFormInValid(form)

    def test_registration_with_required_info(self):
        form_dict = self.get_valid_registration_form_dict()
        self.assertFormValid(EventForm(form_dict))

    def test_registration_deadline_after_event_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["registration_deadline_0"] = form_dict["event_start_0"]
        form_dict["registration_deadline_1"] = "09:00"
        self.assertFormInValid(EventForm(form_dict))

    def test_registration_start_after_event_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["registration_start_0"] = form_dict["event_start_0"]
        form_dict["registration_start_1"] = "09:00"
        self.assertFormInValid(EventForm(form_dict))

    def test_deregistration_deadline_after_event_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["deregistration_deadline_0"] = form_dict["event_start_0"]
        form_dict["deregistration_deadline_1"] = "09:00"
        self.assertFormInValid(EventForm(form_dict))

    def test_registration_start_after_deregistration_deadline_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["registration_start_0"] = "2015-09-01"
        form_dict["registration_start_1"] = "07:00"
        form_dict["deregistration_deadline_0"] = form_dict["registration_start_0"]
        form_dict["deregistration_deadline_1"] = "06:00"
        self.assertFormInValid(EventForm(form_dict))

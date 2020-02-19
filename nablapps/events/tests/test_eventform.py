"""
Tests for the EventForm
"""
# pylint: disable=C0111,C0301
from collections import ChainMap

from django.test import TestCase

from nablapps.events.forms import EventForm


class EventFormTestCase(TestCase):
    def assertFormValid(self, form):
        self.assertTrue(
            form.is_valid(), f"Form should be valid but has these errors: {form.errors}"
        )

    def assertFormInValid(self, form):
        self.assertFalse(form.is_valid(), "Form should be invalid but isn't")

    def get_smallest_valid_form(self):
        return {
            "headline": "Headline",
            "event_start": "2015-10-01",
            "location": "Here",
        }

    def get_valid_registration_form_dict(self):
        return ChainMap(
            {
                "registration_required": "1",
                "places": "20",
                "registration_deadline": "2015-09-01",
                "has_queue": "0",
                "penalty": 0,
            },
            self.get_smallest_valid_form(),
        )

    def test_empty_form(self):
        self.assertFormInValid(EventForm({}))

    def test_smallest_valid_form(self):
        self.assertFormValid(EventForm(self.get_smallest_valid_form()))

    def test_event_end_before_event_start(self):
        form_dict = self.get_smallest_valid_form()
        form_dict["event_end"] = "2015-08-01"
        self.assertFormInValid(EventForm(form_dict))

    def test_with_registration_without_required_info(self):
        form_dict = self.get_smallest_valid_form()
        form_dict["registration_required"] = "1"
        self.assertFormInValid(EventForm(form_dict))

    def test_registration_with_required_info(self):
        form_dict = self.get_valid_registration_form_dict()
        self.assertFormValid(EventForm(form_dict))

    def test_registration_deadline_after_event_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["registration_deadline"] = "2015-11-01"
        self.assertFormInValid(EventForm(form_dict))

    def test_registration_start_after_event_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["registration_start"] = "2015-11-01"
        self.assertFormInValid(EventForm(form_dict))

    def test_deregistration_deadline_after_event_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["deregistration_deadline"] = "2015-11-01"
        self.assertFormInValid(EventForm(form_dict))

    def test_deregistration_deadline_before_registration_start_is_invalid(self):
        form_dict = self.get_valid_registration_form_dict()
        form_dict["registration_start"] = "2015-08-01"
        form_dict["deregistration_deadline"] = "2015-07-01"
        self.assertFormInValid(EventForm(form_dict))

    def test_ignore_registration_fields(self):
        form_dict = self.get_smallest_valid_form()
        # This field will be ignored, even though it contains an error,
        # because "registration_required" is not True
        form_dict["registration_start"] = "erroneous datetime"
        self.assertFormValid(EventForm(form_dict))

# -*- coding: utf-8 -*-

import operator

from django.forms import SplitDateTimeField, BooleanField, ValidationError
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Event
from news.forms import NewsForm
from news.forms import NewsCharField as EventCharField

# Hvilke datoformat som aksepteres fra brukeren.
DATE_FORMATS = ('%Y-%m-%d',
                '%d/%m/%Y',
                '%d/%m/%y',
                '%d.%m.%Y',
                '%d.%m.%y',
                '%d.%n.%Y',
                '%d.%n.%y',)

TIME_FORMATS = ('%H:%M:%S',
                '%H:%M',
                '%H',)


class EventSplitDateTimeField(SplitDateTimeField):
    default_error_messages = {
        'invalid_date': u'Ugyldig dato. Prøv formatet "DD.MM.ÅÅÅÅ".',
        'invalid_time': u'Ugyldig tid. Prøv formatet "HH:MM".',
        'required': u'Dette tidspunktet er påkrevd.',
        }

    def __init__(self, *args, **kwargs):
        kwargs.update(input_date_formats=DATE_FORMATS,
                      input_time_formats=TIME_FORMATS,
                      widget=AdminSplitDateTime())
        super(EventSplitDateTimeField, self).__init__(*args, **kwargs)


class EventForm(NewsForm):
    # Spesifiser datowidget og aksepterte datoformat.
    event_start = EventSplitDateTimeField(required=True, label="Starter")
    event_end = EventSplitDateTimeField(required=False, label="Slutter")
    registration_start = EventSplitDateTimeField(required=False, label="Påmelding åpner")
    registration_deadline = EventSplitDateTimeField(required=False, label="Påmelding stenger")
    deregistration_deadline = EventSplitDateTimeField(required=False, label="Avmelding stenger")

    location = EventCharField(label="Sted")
    has_queue = BooleanField(
        required=False,
        label="Har venteliste",
        help_text=("Hvis arrangementet har venteliste, går det ann å melde seg på selv etter at det er fullt. "
                   "Man havner da på venteliste, og blir automatisk meldt på om det blir ledig."))

    registration_required = BooleanField(required=False, label="Registrering kreves")

    # Fields required when registration_required is set
    required_registration_fields = ("places", "registration_deadline", "has_queue")

    registration_fields = required_registration_fields + ("deregistration_deadline", "has_queue")

    # Restrict order of the above DateTimes
    datetime_restrictions = (
        # ("field_to_validate", "before/after", "field_to_compare_with"),
        ("event_end", "after", "event_start"),
        ("registration_start", "before", "event_start"),
        ("registration_deadline", "before", "event_start"),
        ("registration_deadline", "after", "registration_start"),
        ("deregistration_deadline", "before", "event_start"),
        ("deregistration_deadline", "after", "registration_start"),
    )

    class Meta(NewsForm.Meta):
        model = Event

    def clean(self):
        self._validate_datetime_order()
        cleaned_data = self.cleaned_data
        registration_required = cleaned_data.get("registration_required")

        if registration_required:
            self._assert_required_registration_fields_supplied()
        else:
            self._ignore_registration_fields()
        return cleaned_data

    def _validate_datetime_order(self):
        """Check if the datetime fields have the correct order."""
        comparison_dict = {
            "after": (operator.gt, '"%(field1)s" må ikke være tidligere enn "%(field2)s".'),
            "before": (operator.lt, '"%(field1)s" må ikke være senere enn "%(field2)s".'),
            }

        for field1, comparison, field2 in self.datetime_restrictions:
            date1 = self.cleaned_data.get(field1)
            date2 = self.cleaned_data.get(field2)
            if not (date1 and date2):
                continue

            op, msg = comparison_dict.get(comparison)
            if not op(date1, date2):
                error = ValidationError(msg, params={"field1": self.fields[field1].label,
                                                     "field2": self.fields[field2].label})
                self.add_error(field1, error)

    def _assert_required_registration_fields_supplied(self):
        for field in self.required_registration_fields:
            if (not self.cleaned_data.get(field)) and (field not in self._errors):
                error = ValidationError('Feltet "%(field)s" er påkrevd når %(field2)s er valgt.',
                                        params={"field": self.fields[field].label,
                                                "field2": self.fields["registration_required"].label})
                self.add_error(field, error)

    def _ignore_registration_fields(self):
        for name in self.registration_fields:
            self.cleaned_data[name] = None
            # Ignorer feil relatert til feltet.
            if name in self._errors:
                del self._errors[name]

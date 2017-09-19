import operator

from django.forms import BooleanField, ValidationError
from django.forms.models import fields_for_model

from content.forms import ContentForm
from .models import Event


class EventForm(ContentForm):
    has_queue = BooleanField(
        required=False,
        label="Har venteliste",
        help_text=("Hvis arrangementet har venteliste, går det ann å melde seg på selv etter at det er fullt. "
                   "Man havner da på venteliste, og blir automatisk meldt på om det blir ledig."))

    # Fields required when registration_required is set
    required_registration_fields = ("places", "registration_deadline", "has_queue")
    registration_fields = required_registration_fields + ("deregistration_deadline", "registration_start")

    # Restrict order of the DateTimeFields
    datetime_restrictions = (
        # ("field_to_validate", "before/after", "field_to_compare_with"),
        ("event_end", "after", "event_start"),
        ("registration_start", "before", "event_start"),
        ("registration_deadline", "before", "event_start"),
        ("registration_deadline", "after", "registration_start"),
        ("deregistration_deadline", "before", "event_start"),
        ("deregistration_deadline", "after", "registration_start"),
    )

    class Meta:
        model = Event
        fields = fields_for_model(Event)

    def clean(self):
        self._validate_datetime_order()

        registration_required = self.cleaned_data.get("registration_required")
        if registration_required:
            self._assert_required_registration_fields_supplied()
        else:
            self._ignore_registration_fields()
        return self.cleaned_data

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
            if self.cleaned_data.get(field) is None and (field not in self._errors):
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

# -*- coding: utf-8 -*-

# arrangement/forms.py

from django import forms
from arrangement.models import Event, Happening
from innhold.forms import SiteContentForm
import datetime

DATE_FORMATS = ['%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y %H:%M',
                '%d/%m/%Y',
                '%d/%m/%y %H:%M:%S',
                '%d/%m/%y %H:%M',
                '%d/%m/%y',]

DATE_FORMAT = DATE_FORMATS[1]

class HappeningForm(SiteContentForm):
    event_start = forms.DateTimeField(input_formats=DATE_FORMATS,
                                      widget = forms.DateTimeInput(format=DATE_FORMAT),
                                      required=True,)
    event_end = forms.DateTimeField(input_formats=DATE_FORMATS,
                                    widget = forms.DateTimeInput(format=DATE_FORMAT),
                                    required=False,)

    class Meta(SiteContentForm.Meta):
        model = Happening


class EventForm(HappeningForm):
    registration_required = forms.BooleanField(required=False)
    has_queue = forms.BooleanField(required=False)

    class Meta(HappeningForm.Meta):
        model = Event

    def clean(self):
        cleaned_data = self.cleaned_data
        event_start = cleaned_data.get("event_start")
        registration_required = cleaned_data.get("registration_required")
        places = cleaned_data.get("places")
        registration_deadline = cleaned_data.get("registration_deadline")
        deregistration_deadline = cleaned_data.get("deregistration_deadline")
        has_queue = cleaned_data.get("has_queue")

        if registration_required is True:
            if not places and "places" not in self._errors:
                self._errors["places"] = self.error_class([u'Antall plasser er påkrevd når "påmelding" er valgt.'])

            if not registration_deadline and "registration_deadline" not in self._errors:
                self._errors["registration_deadline"] = self.error_class([u'Påmeldingsfrist er påkrevd når "påmelding" er valgt.'])
            elif event_start and registration_deadline and registration_deadline > event_start:
                self._errors["registration_deadline"] = self.error_class([u'Påmeldingsfrist må ikke være senere enn arrangementstart.'])

            if event_start and deregistration_deadline and deregistration_deadline > event_start:
                self._errors["deregistration_deadline"] = self.error_class([u"Avmeldingsfrist må ikke være senere enn arrangementstart."])

            if has_queue is None and "has_queue" not in self._errors:
                cleaned_data["has_queue"] = False
        else:
            field_names = (
                "places",
                "registration_deadline",
                "deregistration_deadline",
                "has_queue",
                )
            for name in field_names:
                cleaned_data[name] = None
                if name in self._errors:
                    del self._errors[name]

        return cleaned_data

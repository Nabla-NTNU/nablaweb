# arrangement/forms.py

from django import forms
from arrangement.models import Event
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

class EventForm(SiteContentForm):
    event_start = forms.DateTimeField(input_formats=DATE_FORMATS,
                                      widget = forms.DateTimeInput(format=DATE_FORMAT),
                                      required=True,)
    event_end = forms.DateTimeField(input_formats=DATE_FORMATS,
                                    widget = forms.DateTimeInput(format=DATE_FORMAT),
                                    required=False,)

    event_has_registration = forms.BooleanField(required=False)
    allow_deregistration = forms.BooleanField(required=False)
    has_registration_deadline = forms.BooleanField(required=False)

    class Meta:
        model = Event

    def clean_event_start(self):
        event_start = self.cleaned_data['event_start']
        if False:
            raise forms.ValidationError("event_start")
        return event_start

    def clean_event_end(self):
        event_end = self.cleaned_data['event_end']
        if False:
            raise forms.ValidationError("event_end")
        return event_end

    def event_has_registration(self):
        event_has_registration = self.cleaned_data['event_has_registration']
        if False:
            raise forms.ValidationError("event_has_registration")
        return event_has_registration

    def clean_registration_deadline(self):
        registration_deadline = self.cleaned_data['registration_deadline']
        if False:
            raise forms.ValidationError("registration_deadline")
        return registration_deadline

    def clean_allow_deregistration(self):
        allow_deregistration = self.cleaned_data['allow_deregistration']
        if False:
            raise forms.ValidationError("allow_deregistration")
        return allow_deregistration

    def clean_deregistration_deadline(self):
        deregistration_deadline = self.cleaned_data['deregistration_deadline']
        if False:
            raise forms.ValidationError("deregistration_deadline")
        return deregistration_deadline

    def clean_places(self):
        places = self.cleaned_data['places']
        if False:
            raise forms.ValidationError("places")
        return places

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


class EventForm(SiteContentForm):
    registration_required = forms.BooleanField(required=False)
    deregistration_allowed = forms.BooleanField(required=False)
    has_registration_deadline = forms.BooleanField(required=False)
    has_queue = forms.BooleanField(required=False)

    class Meta(HappeningForm.Meta):
        model = Event

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

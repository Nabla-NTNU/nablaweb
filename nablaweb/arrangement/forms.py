# arrangement/forms.py

from django import forms
from arrangement.models import Event

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

class EventForm(forms.ModelForm):
    event_start = forms.DateTimeField(input_formats=DATE_FORMATS,
                                      widget = forms.DateTimeInput(format=DATE_FORMAT),
                                      required=True,)
    event_end = forms.DateTimeField(input_formats=DATE_FORMATS,
                                    widget = forms.DateTimeInput(format=DATE_FORMAT),
                                    required=True,)

    allow_deregistration = forms.BooleanField(required=False)
    has_registration_deadline = forms.BooleanField(required=False)

    class Meta:
        model = Event
        exclude = (
            'permissions_string',
            'waiting_list',
            'attending_users',
            'is_closed',
            )

    def clean_image(self):
        image = self.cleaned_data['image']
        if False:
            raise forms.ValidationError("image")
        return image

    def clean_alternative_id(self):
        alternative_id = self.cleaned_data['alternative_id']
        if False:
            raise forms.ValidationError("alternative_id")
        return alternative_id

    def clean_event_type(self):
        event_type = self.cleaned_data['event_type']
        if False:
            raise forms.ValidationError("event_type")
        return event_type

    def clean_organizer(self):
        organizer = self.cleaned_data['organizer']
        if False:
            raise forms.ValidationError("organizer")
        return organizer

    def clean_url(self):
        url = self.cleaned_data['url']
        if False:
            raise forms.ValidationError("url")
        return url

    def clean_event_end(self):
        event_end = self.cleaned_data['event_end']
        if False:
            raise forms.ValidationError("event_end")
        return event_end

    def clean_places(self):
        places = self.cleaned_data['places']
        if False:
            raise forms.ValidationError("places")
        return places

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


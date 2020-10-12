from django import forms

from .models import QrEvent
from nablapps.events.models.event import Event

# from multi_email_field.forms import MultiEmailField

class EventForm(forms.Form):
    nabla_event_field = forms.ModelChoiceField(queryset=Event.objects.all())
    event_name_field = forms.CharField(required=True)

    def get_nabla_event(self):
        cd = self.cleaned_data
        nabla_event = cd["nabla_event_field"]
        return nabla_event

    def get_event_name(self):
        cd = self.cleaned_data
        qr_event_name = cd["event_name_field"]
        return qr_event_name
        


class EmailForm(forms.Form):
    email_field = forms.CharField(
        required=False, widget=forms.Textarea
    )  # MultiEmailField()

    def get_emails(self):
        cd = self.cleaned_data
        emails = cd["email_field"]
        return emails

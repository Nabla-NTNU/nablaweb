from django import forms
#from multi_email_field.forms import MultiEmailField

from .models import QrEvent

class EmailForm(forms.Form):
    qr_event_field = forms.ModelChoiceField(queryset=QrEvent.objects.all())
    email_field = forms.CharField(required=True, widget=forms.Textarea) #MultiEmailField()


    def get_qr_event(self):
        cd = self.cleaned_data
        qr_event = cd['qr_event_field']
        return qr_event


    def get_emails(self):
        cd = self.cleaned_data
        emails = cd['email_field']
        return emails

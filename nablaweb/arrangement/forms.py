# arrangement/forms.py

from django import forms

DATE_FORMAT = '%d-%m-%Y %H:%M'

class EventForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    summary = forms.CharField(max_length=1000, required=True)
    body = forms.CharField(max_length=5000, required=True)

    location = forms.CharField(max_length=100, required=True)
    event_start = forms.DateTimeField(required=True)
    event_start.widget = forms.DateInput(format=DATE_FORMAT)
    event_start.input_formats = (DATE_FORMAT,)

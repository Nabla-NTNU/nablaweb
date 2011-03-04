# arrangement/forms.py

from django import forms

DATE_FORMAT = '%d-%m-%Y %H:%M'

class SimpleEventForm(forms.Form):
    title = forms.CharField(max_length=100)
    summary = forms.CharField(max_length=1000, required=False)
    body = forms.CharField(max_length=5000, required=False)

    location = forms.CharField(max_length=100)
    time = forms.DateTimeField()
    time.widget = forms.DateInput(format=DATE_FORMAT)
    time.input_formats = (DATE_FORMAT,)

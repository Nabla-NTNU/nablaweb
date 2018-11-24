from django import forms
from ..models.code_golf import CodeTask

class Code_golf_form(forms.Form):
    submitted_code = forms.CharField(widget=forms.HiddenInput, required=True)
    submitted_output = forms.CharField(widget=forms.HiddenInput, required=True)

    def get_submitted_code(self):
        cd = self.cleaned_data
        submitted_code = cd['submitted_code']
        return submitted_code

    def get_submitted_output(self):
        cd = self.cleaned_data 
        submitted_output = cd['submitted_output']
        return submitted_output

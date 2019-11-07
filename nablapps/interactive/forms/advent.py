from django import forms

class SantaForm(forms.Form):
    santa_id = forms.CharField(
        max_length = 1,
        required = True,
    )

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Brukernavn")
    password = forms.CharField(widget=forms.PasswordInput, label="Passord", required=False)

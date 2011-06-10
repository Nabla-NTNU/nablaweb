from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile

from django.contrib.auth.models import User
from accounts.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label="Brukernavn")
    password = forms.CharField(widget=forms.PasswordInput, label="Passord", required=False)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)



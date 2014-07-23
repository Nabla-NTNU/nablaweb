# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.forms import DateField, DateInput
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

import subprocess

from .models import NablaUser

class SearchForm(forms.Form):
    searchstring = forms.CharField(max_length=50)


class UserForm(forms.ModelForm):
    class Meta:
        model = NablaUser
        fields = ('first_name',
              'last_name',
              'email',
              'ntnu_card_number',
              'avatar',
              'telephone',
              'cell_phone',
              'address',
              'mail_number',
              'wants_email',
              'web_page',
              'birthday',
              'about')

    DATE_FORMATS = ['%d/%m/%Y','%d.%m.%Y','%y-%m-%d','%d/%m/%y','%d.%m.%y','%Y-%m-%d']
    birthday = DateField(label="Bursdag", required=False, widget=DateInput(attrs={'placeholder': 'DD.MM.YY', 'class': 'date'}, format='%d.%m.%y'),\
    input_formats=DATE_FORMATS)


def is_ntnu_username(username):
    """Sjekker om brukernavnet finnes i passwd-fila fra en av ntnus studlinuxservere"""
    try:
        regex = '^%s:' % username
        process = subprocess.Popen(['grep',regex, settings.NTNU_PASSWD], shell=False, stdout=subprocess.PIPE)
        return bool(process.communicate()[0])
    # Hvis ikke settings.NTNU_PASSWD finnes  
    # TODO: Ordne med feilmelding her
    except:
        return False


class RegistrationForm(forms.Form):
    username = forms.CharField(label="NTNU-brukernavn", required=True)

    def clean(self):
        username = self.cleaned_data.get('username')

        try:
            user = NablaUser.objects.get(username=username)
            if user.is_active:
                raise forms.ValidationError(("Denne brukeren er allerede aktivert. Hvis du ikke husker passordet ditt kan bruke"))
            else:
                return self.cleaned_data

        except NablaUser.DoesNotExist:
            raise forms.ValidationError(("Brukernavn ikke registrert i nabladatabase"))
            if is_ntnu_username(username):
                return self.cleaned_data
            else:
                raise forms.ValidationError(("Ikke et NTNU-brukernavn."))


# Forms for admin
class NablaUserChangeForm(UserChangeForm):
    class Meta:
        model = NablaUser
        fields = '__all__'

class NablaUserCreationForm(UserCreationForm):
    class Meta:
        model = NablaUser
        fields = ('username',)

    # Denne metoden fra UserCreationForm kræsjer i django 1.6.
    # I django 1.7 er den fjernet
    # TODO: sjekk om den kan fjernes herfra i django 1.7 
    def clean_username(self):
        return self.cleaned_data["username"]

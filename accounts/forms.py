# -*- coding: utf-8 -*-
from datetime import datetime as dt

from django import forms
from django.forms import DateField
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import NablaUser, RegistrationRequest


class UserForm(forms.ModelForm):
    """Used for updating the profile information of a user.

    It is meant to be used by the user, not in the admin interface.
    """
    class Meta:
        model = NablaUser
        fields = (
            'first_name',
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

    # Use a select widget for picking date of birth
    birthday = DateField(
        label="Bursdag",
        required=False,
        widget=SelectDateWidget(years=list(range(dt.now().year-15, dt.now().year-40, -1))),
    )


class RegistrationForm(forms.Form):
    """Form used to activate a new user.

    Validates a username that has been supplied by a new user.
    The user-object has to have been created, but not activated.
    That is webkom must create it first.
    """
    username = forms.CharField(label="NTNU-brukernavn", required=True)

    def clean(self):
        username = self.cleaned_data.get('username')

        try:
            user = NablaUser.objects.get(username=username)
        except NablaUser.DoesNotExist:
            request = RegistrationRequest()
            request.username = username
            request.clean()
            request.save()
            raise forms.ValidationError("Denne brukeren er ikke registrert. "
                                        "En forespørsel har blitt opprettet og "
                                        "du vil få en mail hvis den blir godkjent.")

        if user.is_active:
            raise forms.ValidationError("Denne brukeren er allerede aktivert.")

        return self.cleaned_data


# Forms for admin
class NablaUserChangeForm(UserChangeForm):
    class Meta:
        model = NablaUser
        fields = '__all__'


class NablaUserCreationForm(UserCreationForm):
    class Meta:
        model = NablaUser
        fields = ('username',)

    # Overriding this method because the original uses contrib.auth.models.User
    # instead of NablaUser
    def clean_username(self):
        return self.cleaned_data["username"]


class InjectUsersForm(forms.Form):
    title = "Putt brukernavn i databasen."
    data = forms.CharField(
        widget=forms.Textarea,
        label="Data"
    )

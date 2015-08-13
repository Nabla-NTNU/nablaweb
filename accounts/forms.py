# -*- coding: utf-8 -*-
from django import forms
from django.forms import DateField
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import NablaUser


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
        # We assume that the user is born between 1980 and 1999 (so someone has to fix this before 2019)
        widget=SelectDateWidget(years=reversed(range(1980, 2000))),
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
            raise forms.ValidationError(
                "Brukernavn ikke registrert i nabladatabase. "
                "Send en epost til webkom@nabla.ntnu.no så lager vi en bruker til deg.")

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

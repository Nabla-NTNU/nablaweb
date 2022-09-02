from datetime import datetime as dt

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.widgets import SelectDateWidget

from .models import FysmatClass, NablaUser


class UserForm(forms.ModelForm):
    """Used for updating the profile information of a user.

    It is meant to be used by the user, not in the admin interface.
    """

    class Meta:
        model = NablaUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "ntnu_card_number",
            "avatar",
            "cropping",
            "telephone",
            "cell_phone",
            "address",
            "mail_number",
            "wants_email",
            "web_page",
            "birthday",
            "about",
            "darkmode",
        )

    # Use a select widget for picking date of birth
    birthday = forms.DateField(
        label="Bursdag",
        required=False,
        widget=SelectDateWidget(
            years=list(range(dt.now().year - 15, dt.now().year - 40, -1))
        ),
    )

    ntnu_card_number = forms.CharField(
        help_text=(
            "Dette er et 7-10-sifret nummer på baksiden av kortet. "
            "På nye kort er dette sifrene etter EM. "
            "På gamle kort er dette sifrene nede til venstre. "
            "Det kan brukes of å identifisere deg på bedriftspresentasjoner og andre arrangementer. "
            "<img style='padding-top:10px;' alt=' ' src='/static/img/ntnu_card_number.png' height = 180> </img>"
        )
    )

    darkmode = forms.BooleanField(
        required=False,
        help_text="Darkmode er fortsatt under utvikling",
    )


class RegistrationForm(forms.Form):
    """Form used to activate a new user or send a registration request."""

    username = forms.CharField(label="NTNU-brukernavn", required=True)

    first_name = forms.CharField(label="Fornavn", required=True)

    last_name = forms.CharField(label="Etternavn", required=True)


# Forms for admin
class NablaUserChangeForm(UserChangeForm):
    class Meta:
        model = NablaUser
        fields = "__all__"


class NablaUserCreationForm(UserCreationForm):
    class Meta:
        model = NablaUser
        fields = ("username",)

    # Overriding this method because the original uses contrib.auth.models.User
    # instead of NablaUser
    def clean_username(self):
        return self.cleaned_data["username"]


class InjectUsersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fysmat_class"] = forms.ChoiceField(
            required=False,
            choices=[("", "Ingen klasse")]
            + [(m.name, m.name) for m in FysmatClass.objects.all()],
            label="Klasse",
        )

    title = "Putt brukernavn i databasen."
    data = forms.CharField(widget=forms.Textarea, label="Data")
    fysmat_class = forms.ChoiceField(
        required=False,
        label="Klasse",
        choices=(),
    )

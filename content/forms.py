from django.forms import BooleanField, ModelForm


class ContentForm(ModelForm):
    listen = BooleanField(
        label="Overvåk",
        help_text="Få notifikasjoner hvis objektet endres",
        required=False
    )

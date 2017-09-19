from django.forms import BooleanField, ModelForm

from content.models import News
from django.forms.models import fields_for_model


class ContentForm(ModelForm):
    listen = BooleanField(
        label="Overvåk",
        help_text="Få notifikasjoner hvis objektet endres",
        required=False
    )


class NewsForm(ContentForm):

    class Meta:
        model = News
        fields = fields_for_model(News)

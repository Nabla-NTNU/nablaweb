from django.forms.models import fields_for_model, ModelForm
from .models import News


class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = fields_for_model(News)

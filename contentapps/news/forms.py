from django.forms.models import fields_for_model
from content.forms import ContentForm
from .models import News


class NewsForm(ContentForm):

    class Meta:
        model = News
        fields = fields_for_model(News)

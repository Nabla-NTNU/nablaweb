# -*- coding: utf-8 -*-


from django.forms import ModelForm
import content.widgets as widgets
from .models import News


class NewsForm(ModelForm):
    #body = CharField(label="Brødtekst", widget=widgets.MarkdownEditor)

    class Meta:
        model = News
        fields = '__all__'

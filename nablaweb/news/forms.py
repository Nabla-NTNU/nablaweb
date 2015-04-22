# -*- coding: utf-8 -*-


from django.forms import ModelForm, CharField, SplitDateTimeWidget, DateInput, TimeInput
import content.widgets as widgets
from news.models import News


class NewsCharField(CharField):
    default_error_messages = {
        'required': u'Dette feltet er påkrevd.',
        }


class NewsForm(ModelForm):
    headline = NewsCharField(label="Overskrift")
    #body = CharField(label="Brødtekst", widget=widgets.MarkdownEditor)

    class Meta:
        model = News
        fields = '__all__'


class CustomSplitDateTimeWidget(SplitDateTimeWidget):
    def __init__(self, attrs=None, date_attrs=None, time_attrs=None, date_format=None, time_format=None):
        widgets = (
            DateInput(attrs=date_attrs, format=date_format),
            TimeInput(attrs=time_attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

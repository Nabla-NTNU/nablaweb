# -*- coding: utf-8 -*-


from django.forms import ModelForm, CharField, SplitDateTimeWidget, DateInput, TimeInput
from nablaweb.news.models import News


class NewsCharField(CharField):
    default_error_messages = {
        'required': u'Dette feltet er påkrevd.',
        }


class NewsForm(ModelForm):
    headline = NewsCharField(label="Overskrift")
    class Meta:
        model = News


class CustomSplitDateTimeWidget(SplitDateTimeWidget):
    def __init__(self, attrs=None, date_attrs=None, time_attrs=None, date_format=None, time_format=None):
        widgets = (
            DateInput(attrs=date_attrs, format=date_format),
            TimeInput(attrs=time_attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

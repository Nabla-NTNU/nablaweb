# -*- coding: utf-8 -*-

from django.forms import ModelForm, CharField, SplitDateTimeWidget, DateInput, TimeInput
from haystack.forms import SearchForm

class NewSearchForm(SearchForm):
    def search(self):
        s = super(NewSearchForm, self).search()
        return s

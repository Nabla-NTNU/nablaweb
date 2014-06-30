# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from jobs.models import Advert, Company

class AdvertForm(ModelForm):
    headline = forms.CharField(help_text="Tittelen på stillingsannonsen. Bør inneholde bedriftens navn")
    class Meta:
        model = Advert

class CompanyForm(ModelForm):
    name = forms.CharField(help_text="Navnet på bedriften")
    class Meta:
        model = Company

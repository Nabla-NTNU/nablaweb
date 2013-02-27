# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from nablaweb.jobs.models import Advert, Company

class AdvertForm(ModelForm):
    headline = forms.CharField(help_text="Tittelen på stillingsannonsen. Bør inneholde bedriftens navn")
    class Meta:
        model = Advert

class CompanyForm(ModelForm):
    name = forms.CharField(help_text="Navnet på bedriften")
    picture = forms.FileField(help_text="Bilder som er større enn 770x250 px ser best ut. Du kan beskjære bildet etter opplasting.", label="Logo", required=False)
    class Meta:
        model = Company

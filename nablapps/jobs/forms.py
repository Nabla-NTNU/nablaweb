from django import forms
from django.forms import ModelForm
from nablapps.jobs.models import Advert, Company


class AdvertForm(ModelForm):
    headline = forms.CharField(
        help_text="Tittelen på stillingsannonsen. Bør inneholde bedriftens navn",
    )

    class Meta:
        model = Advert
        fields = '__all__'


class CompanyForm(ModelForm):
    name = forms.CharField(help_text="Navnet på bedriften")

    class Meta:
        model = Company
        fields = '__all__'

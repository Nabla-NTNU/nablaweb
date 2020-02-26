"""
Forms for jobs app
"""
from django import forms
from django.forms import ModelForm

from nablapps.jobs.models import Advert, Company


class AdvertForm(ModelForm):
    """Form for creating and updating an advert"""

    headline = forms.CharField(
        help_text="Tittelen på stillingsannonsen. Bør inneholde bedriftens navn",
    )

    class Meta:
        model = Advert
        fields = "__all__"


class CompanyForm(ModelForm):
    """Form for creating and updating a Company object"""

    name = forms.CharField(help_text="Navnet på bedriften")

    class Meta:
        model = Company
        fields = "__all__"

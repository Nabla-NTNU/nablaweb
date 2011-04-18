# nyheter/forms.py

from django import forms
from nyheter.models import SiteContent

class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent

class NewsForm(SiteContentForm):
    pass

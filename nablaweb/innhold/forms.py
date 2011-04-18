# innhold/forms.py

from django import forms
from innhold.models import SiteContent

class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent

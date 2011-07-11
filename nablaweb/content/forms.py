from django import forms
from content.models import SiteContent

class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent

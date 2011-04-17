# nyheter/forms.py

from django import forms
from nyheter.models import SiteContent

class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent
        exclude = (
            'created_date',
            'created_by',
            'last_changed_date',
            'last_changed_by',
            )

class NewsForm(SiteContentForm):
    pass

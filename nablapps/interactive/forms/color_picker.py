from django import forms
from ..models import validate_color

class ColorChoiceForm(forms.Form):
    color = forms.CharField(validators=[validate_color])

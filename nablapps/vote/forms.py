from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Votation, Alternative


AlternativeFormset = inlineformset_factory(
    Votation, Alternative, fields=("text",), can_delete=False
)

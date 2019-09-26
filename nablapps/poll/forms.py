"""
Forms for poll app
"""
from nablapps.core.admin import ChangedByMixin
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Poll, Choice

ChoiceFormSet = inlineformset_factory(Poll, Choice, fields=('choice',), can_delete=False)


class PollForm(ChangedByMixin, ModelForm):
    class Meta:
        model = Poll
        fields = ('question', 'answer',)
        exclude = ('delete',)
        help_texts = { 'answer': 'Valgfritt', }


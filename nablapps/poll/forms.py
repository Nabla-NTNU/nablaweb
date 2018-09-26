"""
Forms for poll app
"""
from datetime import datetime
from itertools import takewhile, count

from content.admin import ChangedByMixin
from django import forms
from django.forms.models import inlineformset_factory
from .models import Poll, Choice

ChoiceFormSet = inlineformset_factory(Poll, Choice, fields=('choice',))


def get_choice_field_iter():
    """ Returns an infinite iterator of the choice field names for PollForm"""
    return map('choice_{}'.format, count(start=1))


class PollForm(ChangedByMixin, forms.ModelForm):
    """Form for creating and updating a poll"""
    choice_1 = forms.CharField(
        max_length=80,
        label='Alternativ 1',
        required=True
    )

    choice_2 = forms.CharField(
        max_length=80,
        label='Alternativ 2',
        required=False
    )

    choice_3 = forms.CharField(
        max_length=80,
        label='Alternativ 3',
        required=False
    )

    choice_4 = forms.CharField(
        max_length=80,
        label='Alternativ 4',
        required=False
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = ChoiceFormSet(
            instance=self.instance
        )
        choices = self.instance.choices.all()
        self.initial.update(
            dict(zip(get_choice_field_iter(), choices))
        )
        self.user = user

    def save(self, commit=True):

        self.instance.is_current = False
        self.instance.is_user_poll = True
        if not self.instance.created_by and self.user is not None:
            self.instance.created_by = self.user
        self.instance.publication_date = datetime.now()
        self.instance.save()

        related = self.instance.choices

        # Iterator of the supplied choices
        updated_choices = map(self.cleaned_data.get, get_choice_field_iter())

        # Go through each choice and update it.
        # Delete it if the field is empty
        for choice in related.all():
            new_name = next(updated_choices)
            if new_name:
                choice.choice = new_name
                choice.save()
            else:
                choice.delete()

        # Add the remaining new choices until reaching an empty field
        for new_name in takewhile(bool, updated_choices):
            related.create(choice=new_name)

        return super().save(commit)

    class Meta:
        model = Poll
        fields = ('question', 'answer',)
        help_texts = {
            'answer': 'Valgfritt',
            }

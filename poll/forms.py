# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.forms.models import inlineformset_factory
from .models import *
from content.admin import ChangedByMixin

ChoiceFormSet = inlineformset_factory(Poll, Choice, fields=('choice',))


class PollForm(ChangedByMixin, forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = ChoiceFormSet(
            instance=self.instance
        )
        choices = self.instance.choices.all()
        i = 1
        for c in choices:
            self.initial['choice_'+str(i)] = c.choice
            i += 1

    def save(self, commit=True):
        user = self.view.request.user

        self.instance.is_current = False
        self.instance.is_user_poll = True
        if not self.instance.created_by:
            self.instance.created_by = user
        self.instance.publication_date = datetime.now()

        related = self.instance.choices
        updated_choices = []

        i = 1
        while i <= 20:
            choice = self.cleaned_data.get('choice_' + str(i))
            if not choice:
                break
            updated_choices.append(choice)
            i += 1

        choices = related.all()
        for i in range(0, len(updated_choices)):
            new_name = updated_choices[i]
            try:
                choice = choices[i]
            except IndexError:
                choice = None
            if new_name:
                if choice:
                    choice.choice = new_name
                    choice.save()
                else:
                    if not self.instance.id:
                        self.instance.save()
                    related.create(
                        choice=new_name
                    )
            else:
                if choice:
                    related.remove(choice)
                break

        return super().save(commit)

    class Meta:
        model = Poll
        fields = ('question',
                  )

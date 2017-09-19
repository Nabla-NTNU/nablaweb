from django.contrib import admin
from .models import GeneralOptions
from django import forms
from contentapps.news.models import News


class GeneralOptionsForm(forms.ModelForm):
    
    news = forms.ModelChoiceField(
        queryset=News.objects.order_by('-created_date'),
        required=False,
        label="Hovednyhet",
        help_text="Nyheten som vises øverst på siden"
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['news'] = instance.main_story
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        options = super(forms.ModelForm, self).save(commit=commit)

        options.main_story = self.cleaned_data['news']
        return options


@admin.register(GeneralOptions)
class GeneralOptionsAdmin(admin.ModelAdmin):
    form = GeneralOptionsForm

    exclude = ['main_story_id', 'main_story_content_type']


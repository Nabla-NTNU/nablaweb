# Forms for creating new threads and messages.
# Channels will be created in admin
from django import forms

from .models import Channel

class ChannelForm(forms.ModelForm):
    #name_field = forms.CharField()
    #description_field = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Channel
        fields = ['group', 'name', 'description']
    def __init__(self, groups=None, **kwargs):
        super().__init__(**kwargs)
        if groups:
            self.fields['group'].queryset = groups
        else:
            # Just want to set an empty query set, so uses Channel just because it's already imported
            self.fields['group'].queryset = Channel.objects.none() 


class ThreadForm(forms.Form):
    title_field = forms.CharField()
    text_field = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.Form):
    message_field = forms.CharField(widget=forms.Textarea)


class JoinChannelsForm(forms.Form):
    selected_channels = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('selected_channels', None)
        super().__init__(*args, **kwargs)
        self.fields['selected_channels'].choices = choices

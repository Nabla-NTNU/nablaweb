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



class ThreadForm(forms.Form):
    title_field = forms.CharField()
    text_field = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.Form):
    message_field = forms.CharField(widget=forms.Textarea)




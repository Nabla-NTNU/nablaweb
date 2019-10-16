# Forms for creating new threads and messages.
# Channels will be created in admin
from django import forms

class ChannelForm(forms.Form):
    name_field = forms.CharField()
    description_field = forms.CharField(widget=forms.Textarea)


class ThreadForm(forms.Form):
    title_field = forms.CharField()
    text_field = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.Form):
    message_field = forms.CharField(widget=forms.Textarea)




from django import forms
from .models import Channel, Thread

class ThreadForm(forms.Form):
    channel_field = forms.ModelChoiceField(queryset=Channel.objects.all())
    thread_starter_field = forms.ModelChoiceField#get current
    title = forms.CharField()
    text_body = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.Form):
    thread_field = forms.ModelsChoiceField(##get current thread
    user_field = forms.ModelsChoiceField#get current
    message_field = forms.CharField(widget=Textarea)




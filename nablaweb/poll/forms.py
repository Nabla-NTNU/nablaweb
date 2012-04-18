from django.forms import ModelForm, widgets
from poll.models import Poll, Choice

class PollForm(Form):
    class Meta:
        model = Poll

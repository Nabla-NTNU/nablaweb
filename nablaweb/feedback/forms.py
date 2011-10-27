from django import forms
from django.contrib.formtools.preview import FormPreview

from math_captcha.forms import MathCaptchaModelForm
from feedback.models import Feedback

class FeedbackModelForm(MathCaptchaModelForm):
    class Meta:
        model = Feedback

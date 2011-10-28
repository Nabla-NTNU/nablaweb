from custom_comments.forms import SimpleCommentForm
from django.contrib.comments.models import Comment

def get_form():
    return SimpleCommentForm

def get_model():
    return Comment

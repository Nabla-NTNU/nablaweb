from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.forms import CommentForm


class SimpleCommentForm(CommentForm):
    class Meta:
        model = Comment
        exclude = ('name', 'email', 'url')

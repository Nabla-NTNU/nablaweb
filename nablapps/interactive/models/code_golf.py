#Models for code_golf
from django.db import models
from datetime import timedelta, datetime
from django.conf import settings


class CodeTask(models.Model):
    title = models.CharField(max_length=100)
    task = models.TextField()
    correct_output = models.TextField(blank=False)

    def __str__(self):
        return self.title

    def get_correct_output(self):
        return self.correct_output

class Result(models.Model):
    """
    Users solution to a CodeTask
    """
    
    task = models.ForeignKey(CodeTask, on_delete=models.CASCADE,)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    solution = models.TextField(default="") # Users code

    @property
    def length(self):
        return len(self.solution.strip()) # Do not count whitespace

    def __str__(self):
        return f"{self.user}'s solution to CodeTask #{self.task.id}"


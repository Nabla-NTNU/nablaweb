#Models for code_golf
from django.db import models
from datetime import timedelta, datetime


class CodeTask(models.Model):
    title = models.CharField(max_length=100)
    task = models.CharField(max_length=200)
    correct_output = models.TextField(blank=False)

    def __str__(self):
        return self.title

    def get_correct_output(self):
        return self.correct_output

class Result(models.Model):
    task = models.ForeignKey(CodeTask, on_delete=models.CASCADE,)
    user = models.CharField(max_length = 100)
    length = models.IntegerField()

    def __str__(self):
        return self.user


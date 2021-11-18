# Models for code_golf
import json

from django import template
from django.db import models
from django.utils import timezone

from nablapps.accounts.models import NablaUser

register = template.Library()


class CodeTask(models.Model):
    title = models.CharField(max_length=100)
    task = models.TextField()
    correct_output = models.TextField(blank=False)

    def __str__(self):
        return self.title

    def get_correct_output(self):
        return self.correct_output

    def get_best_result(self):
        if len(self.result_set.all()) > 0:
            return sorted(self.result_set.all(), key=lambda result: result.length)[0]
        else:
            return None

    @property
    def correct_output_json(self):
        """
        JSON repr of the list of lines in the correct output

        Used to transfer the correct output to the template
        """
        return json.dumps(
            [line.rstrip("\r") for line in self.correct_output.split("\n")]
        )


class Result(models.Model):
    """
    Users solution to a CodeTask
    """

    task = models.ForeignKey(
        CodeTask,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        NablaUser,
        on_delete=models.CASCADE,
    )
    solution = models.TextField(default="")  # Users code
    submitted_at = models.DateTimeField(
        default=timezone.now,
        help_text="The time that the user first submitted code with this score (worse submissions do not update this field)",
    )

    @staticmethod
    def compute_length(submission: str) -> int:
        return len(submission.strip())

    @property
    def length(self):
        return self.compute_length(self.solution.strip())

    def __str__(self):
        return f"{self.user}'s solution to CodeTask #{self.task.id}"

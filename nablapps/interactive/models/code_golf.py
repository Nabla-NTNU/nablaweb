# Models for code_golf
import json

from django import template
from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone

from nablapps.accounts.models import NablaUser

register = template.Library()


class CodeTask(models.Model):
    title = models.CharField(max_length=100)
    task = models.TextField()
    correct_output = models.TextField(blank=False)

    def __str__(self):
        return self.title

    def get_best_result(self):
        return self.result_set.order_by("length").first()

    @property
    def correct_output_json(self):
        """
        JSON repr of the list of lines in the correct output

        Used to transfer the correct output to the template
        """
        return json.dumps(
            [line.rstrip("\r") for line in self.correct_output.split("\n")]
        )


class ResultManager(models.Manager):
    """Manager for Results

    Adds often used queries like best form user etc"""

    def best_by_user(self, task, full_object=False):
        """Get best submission by each user

        full_object: Bool
          If False, return a list of dicts, each with the form {'user': <user_pk>, 'length__min': <length of shortest solution>}
          If True, return a full queryset with the shortest result from each user.
        """
        if not full_object:
            return (
                self.filter(task=task)
                .values(
                    "user",
                    full_name=Concat(
                        "user__first_name", models.Value(" "), "user__last_name"
                    ),
                )
                .annotate(length=models.Min("length"))
            )
        else:
            # This is an advanced query. If you know a shorter way, feel free to
            # change it. We use the OuterRef and Subquery here. In the last
            # expression, we sort of "pass along" the row's user to teh subquery
            # `min_pk`. For each user, we filter the results, and find the
            # shortest one, and return the pk. The [:1] instead of [0] is sort
            # of a "hack" to make the expression legal. [0] will attempt to
            # evaluate the query, resulting in Django complaining we are not
            # inside of a subquery.
            raise Exception("there is something wrong with this implementation")
            min_pk = (
                Result.objects.filter(user=models.OuterRef("user"))
                .order_by("length")
                .values("pk")[:1]
            )
            return Result.objects.filter(pk=models.Subquery(min_pk)).order_by("length")


class Result(models.Model):
    """
    Users solution to a CodeTask

    - TODO consider making user+solution unique together, thus not accepting multiple equal solutions
    """

    class Meta:
        ordering = ("length",)

    objects = ResultManager()
    task = models.ForeignKey(
        CodeTask,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        NablaUser,
        on_delete=models.CASCADE,
    )
    solution = models.TextField(default="")  # Users code
    length = models.IntegerField()
    python_version = models.CharField(max_length=15)
    submitted_at = models.DateTimeField(
        default=timezone.now,
        help_text="The time that the user first submitted code with this score (worse submissions do not update this field)",
    )

    def save(self, *args, **kwargs):
        # Drop newlines etc.
        self.solution = self.solution.strip()
        self.length = self.solution_length(self.solution)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s solution to CodeTask #{self.task.id}"

    @staticmethod
    def solution_length(solution: str) -> int:
        """Count cleaned solution, i.e. after removing 'extra' characters.

        Remove trailing whitespace, replaces \r\n with \n etc, to make the
        competition as fair as possible."""
        return len(solution.strip().replace("\r\n", "\n"))

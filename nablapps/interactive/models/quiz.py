from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse

from .base import InteractionResult, InteractiveElement, Scoreboard


class QuizQuestion(models.Model):
    question = models.TextField(verbose_name="Spørsmål", blank=False)

    quiz = models.ForeignKey(
        to="Quiz", related_name="questions", on_delete=models.CASCADE, unique=False
    )

    correct_alternative = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], verbose_name="Riktig svar"
    )

    alternative_1 = models.CharField(
        max_length=200, verbose_name="Alternativ 1", blank=False
    )

    alternative_2 = models.CharField(
        max_length=200, verbose_name="Alternativ 2", blank=False
    )

    alternative_3 = models.CharField(
        max_length=200, verbose_name="Alternativ 3", blank=False
    )

    alternative_4 = models.CharField(
        max_length=200, verbose_name="Alternativ 4", blank=False
    )

    def __str__(self):
        return str(self.question)


class Quiz(InteractiveElement):
    """
    Represents a quiz.
    """

    default_template = "interactive/quiz.html"

    title = models.CharField(max_length=80, verbose_name="Tittel")

    is_timed = models.BooleanField(verbose_name="Bruk tidsbegrensning?", default=False)

    duration = models.PositiveIntegerField(
        verbose_name="Tidsbegrensning",
        blank=True,
        null=True,
        help_text="Tid til å fullføre quizen målt i sekunder.",
    )

    scoreboard = models.OneToOneField(
        to="QuizScoreboard", related_name="quiz", on_delete=models.CASCADE, null=True
    )

    published = models.BooleanField(
        null=True,
        default=True,
        verbose_name="Publisert",
    )

    spoiler_html = models.TextField(
        default="",
        blank=True,
        verbose_name="Spoiler HTML",
        help_text="HTML som vises til brukeren etter den har sendt inn et svar "
        "på quizen. Vises ikke dersom den står tom.",
    )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizer"

    def save(self, *args, **kwargs):
        if not self.scoreboard:
            self.scoreboard = QuizScoreboard.objects.create()
        return super().save(*args, **kwargs)

    def duration_timedelta(self):
        return timedelta(seconds=self.duration)

    def total_questions(self):
        return self.questions.count()

    def get_absolute_url(self):
        return reverse("quiz", kwargs={"pk": self.id})

    def __str__(self):
        return str(self.title)


class QuestionReply(models.Model):
    """
    Reply to a single question
    """

    question = models.ForeignKey(
        "QuizQuestion",
        on_delete=models.CASCADE,
    )

    alternative = models.PositiveIntegerField(unique=False)

    quiz_reply = models.ForeignKey(
        to="QuizReply", related_name="questions", on_delete=models.CASCADE, null=True
    )

    @property
    def is_correct(self):
        return self.question.correct_alternative == self.alternative


class QuizReplyTimeout(Exception):
    pass


class QuizReply(InteractionResult):
    """
    Reply to an entire quiz
    """

    scoreboard = models.ForeignKey(
        to="QuizScoreboard", on_delete=models.CASCADE, related_name="replies"
    )

    score = models.IntegerField(null=True, blank=True)

    start = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(
        "accounts.NablaUser",
        on_delete=models.CASCADE,
        related_name="interaction_results",
    )

    class Meta:
        verbose_name = "Resultat"
        verbose_name_plural = "Resultater"

    def save(self, **kwargs):
        self.score = self.get_correct_count()
        return super().save(**kwargs)

    @property
    def quiz(self):
        return self.scoreboard.quiz

    def end_time(self):
        return self.start + self.quiz.duration_timedelta() if self.start else None

    def has_timed_out(self):
        return self.quiz.is_timed and self.end_time() < datetime.now()

    def get_absolute_url(self):
        return reverse("quiz_result", kwargs={"pk": self.id})

    def get_correct_count(self):
        return len([q for q in self.questions.all() if q.is_correct])

    def get_question_count(self):
        return self.scoreboard.quiz.total_questions()

    def add_question_replies(self, replies):
        """
        :param replies: list of tuples (question_object, alternative_number)
        :raises QuizReplyTimeout if the quiz is timed and the reply timed out.
        """
        if self.has_timed_out():
            raise QuizReplyTimeout
        for q, alternative in replies:
            QuestionReply.objects.update_or_create(
                question=q,
                quiz_reply=self,
                defaults={
                    "alternative": alternative,
                },
            )


class QuizScoreboard(Scoreboard):
    """
    Quiz scoreboard.
    """

    def get_absolute_url(self):
        return reverse("quiz_score", kwargs={"pk": self.id})

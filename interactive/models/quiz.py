from django.db import models
from .base import InteractiveElement, Scoreboard, InteractionResult
from django.core.urlresolvers import reverse
from accounts.models import LikeMixin
from content.models.mixins import PublicationManagerMixin


class QuizQuestion(models.Model):
    question = models.TextField(
        verbose_name="Spørsmål",
        blank=False
    )

    quiz = models.ForeignKey(
        to='Quiz',
        related_name="questions",
        unique=False
    )

    correct_alternative = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4')
        ],
        verbose_name="Riktig svar"
    )

    alternative_1 = models.CharField(
        max_length=200,
        verbose_name="Alternativ 1",
        blank=False
    )

    alternative_2 = models.CharField(
        max_length=200,
        verbose_name="Alternativ 2",
        blank=False
    )

    alternative_3 = models.CharField(
        max_length=200,
        verbose_name="Alternativ 3",
        blank=False
    )

    alternative_4 = models.CharField(
        max_length=200,
        verbose_name="Alternativ 4",
        blank=False
    )

    def __str__(self):
        return str(self.question)


class Quiz(PublicationManagerMixin, LikeMixin, InteractiveElement):
    """
    Represents a quiz.
    """

    default_template = "interactive/quiz.html"

    title = models.CharField(
        max_length=80,
        verbose_name="Tittel"
    )

    is_timed = models.BooleanField(
        verbose_name="Bruk tidsbegrensning?",
        default=False
    )

    duration = models.PositiveIntegerField(
        verbose_name="Tidsbegrensning",
        blank=True,
        null=True,
        help_text="Tid til å fullføre quizen målt i sekunder."
    )

    scoreboard = models.OneToOneField(
        to='QuizScoreboard',
        related_name="quiz",
        null=True
    )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizer"

    def save(self, *args, **kwargs):
        if not self.scoreboard:
            self.scoreboard = QuizScoreboard.objects.create()
        return super().save(*args, **kwargs)

    def total_questions(self):
        return self.questions.count()

    def get_absolute_url(self):
        return reverse("quiz", kwargs={'pk': self.id})

    def __str__(self):
        return str(self.title)


class QuestionReply(models.Model):
    """
    Reply to a single question
    """

    question = models.ForeignKey(
        'QuizQuestion',
    )

    alternative = models.PositiveIntegerField(
        unique=False
    )

    quiz_reply = models.ForeignKey(
        to='QuizReply',
        related_name="questions",
        null=True
    )

    @property
    def is_correct(self):
        return self.question.correct_alternative == self.alternative


class QuizReply(InteractionResult):
    """
    Reply to an entire quiz
    """

    scoreboard = models.ForeignKey(
        to='QuizScoreboard',
        related_name="replies"
    )

    score = models.IntegerField(
        null=True,
        blank=True
    )

    start = models.DateTimeField(
        blank=True,
        null=True
    )

    user = models.ForeignKey(
        'accounts.NablaUser',
        related_name="interaction_results"
    )

    class Meta:
        verbose_name = "Resultat"
        verbose_name_plural = "Resultater"

    def save(self, **kwargs):
        self.score = self.get_correct_count()
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('quiz_result', kwargs={'pk': self.id})

    def get_correct_count(self):
        return len([q for q in self.questions.all() if q.is_correct])

    def get_question_count(self):
        return self.scoreboard.quiz.total_questions()


class QuizScoreboard(Scoreboard):
    """
    Quiz scoreboard.
    """

    def get_absolute_url(self):
        return reverse("quiz_score", kwargs={'pk': self.id})

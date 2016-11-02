from django.db import models
from .base import InteractiveElement, InteractionResult
from accounts.models import NablaUser
from com.models import Committee
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from random import choice
from django.conf import settings


class AdventDoor(InteractiveElement):
    """
    An element of the advent calendar.
    """

    number = models.IntegerField(
        verbose_name="Nummer"
    )

    content = models.TextField(
        verbose_name="Innhold",
        blank=True
    )

    committee = models.ForeignKey(
        Committee,
        blank=True,
        verbose_name="Komité",
        null=True
    )

    winner = models.ForeignKey(
        NablaUser,
        verbose_name="Vinner",
        blank=True,
        null=True,
        related_name="advent_doors_won"
    )

    calendar = models.ForeignKey(
        'interactive.AdventCalendar',
        verbose_name="Kalender"
    )

    is_lottery = models.BooleanField(
        default=False,
        verbose_name="Har trekning"
    )

    is_text_response = models.BooleanField(
        default=False,
        verbose_name="Har tekstsvar"
    )

    short_description = models.CharField(
        max_length=200,
        verbose_name="Kort beskrivelse",
        null=True,
        blank=True
    )

    image = models.ImageField(
        verbose_name="Bilde",
        null=True,
        blank=True
    )

    quiz = models.ForeignKey(
        'interactive.Quiz',
        verbose_name="Lenket quiz",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Adventsluke"
        verbose_name_plural = "Adventsluker"
        unique_together = ('number','calendar',)

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse("advent_door", kwargs={
            'year': self.calendar.year,
            'number': self.number
        })

    @property
    def date(self):
        return self.calendar.first + timedelta(days=(self.number-1))

    @property
    def is_published(self):
        if settings.DEBUG:
            return True
        return datetime.now() >= self.date

    @property
    def is_today(self):
        return datetime.now() >= self.date and datetime.now() <= self.date + timedelta(days=1) 

    def choose_winner(self):
        if self.is_lottery and self.is_published:
            self.winner = choice(self.participation.all()).user


class AdventCalendar(models.Model):

    year = models.IntegerField(
        verbose_name="År",
        unique=True
    )

    template = models.CharField(
        max_length=100,
        verbose_name="Template",
        default="interactive/advent_base.html"
    )

    @property
    def first(self):
        return datetime(year=self.year, day=1, month=12)

    class Meta:
        verbose_name = "Adventskalender"
        verbose_name_plural = "Adventskalendere"

    def get_absolute_url(self):
        return reverse("advent_calendar", kwargs={'year': self.year})

    def __str__(self):
        return str(self.year)


class AdventParticipation(InteractionResult):

    text = models.TextField(
        null=True
    )

    door = models.ForeignKey(
        AdventDoor,
        related_name="participation"
    )

    user = models.ForeignKey(
        NablaUser
    )



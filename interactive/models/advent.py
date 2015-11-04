from django.db import models
from .base import InteractiveElement
from accounts.models import NablaUser
from com.models import Committee
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta


class AdventDoor(InteractiveElement):
    """
    An element of the advent calendar.
    """

    number = models.IntegerField(
        verbose_name="Nummer",
        unique=True
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

    users = models.ManyToManyField(
        NablaUser,
        verbose_name="Deltagende brukere",
        blank=True,
        related_name="advent_participating"
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

    participating_users = models.ManyToManyField(
        'accounts.NablaUser',
        blank=True,
        related_name="participating_in_doors"
    )

    short_description = models.CharField(
        max_length=200,
        verbose_name="Kort beskrivelse",
        null=True
    )

    class Meta:
        verbose_name = "Adventsluke"
        verbose_name_plural = "Adventsluker"

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse("advent_door", kwargs={
            'year': self.calendar.year,
            'number': self.number
        })

    @property
    def date(self):
        return self.calendar.first + timedelta(days=self.number)

    @property
    def is_published(self):
        return datetime.now() >= self.date


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
        return datetime(year=self.year, day=1, month=10)

    class Meta:
        verbose_name = "Adventskalender"
        verbose_name_plural = "Adventskalendere"

    def get_absolute_url(self):
        return reverse("advent_calendar", kwargs={'year': self.year})

    def __str__(self):
        return str(self.year)


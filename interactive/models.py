from django.db import models
from accounts.models import NablaUser
from content.models.mixins import EditableMedia
from com.models import Committee
from django.core.urlresolvers import reverse


class InteractiveElement(EditableMedia, models.Model):
    """
    Model for an element requiring user interaction.
    """

    template = models.CharField(
        max_length=100,
        verbose_name="Template",
        default="interactive/advent_door_base.html"
    )

    class Meta:
        abstract = True


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

    class Meta:
        verbose_name = "Adventskalender"
        verbose_name_plural = "Adventskalendere"

    def get_absolute_url(self):
        return reverse("advent_calendar", kwargs={'year': self.year})

    def __str__(self):
        return str(self.year)




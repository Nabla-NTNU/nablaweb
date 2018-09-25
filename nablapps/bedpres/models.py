"""
BPC-bedpres as a django model
"""
from django.urls import reverse
from django.db import models

from nablapps.events.models.abstract_event import AbstractEvent
from nablapps.jobs.models import Company
from .bpcmixin import BPCEventMixin


class BedPres(BPCEventMixin, AbstractEvent):
    """
    Model representing a bedpress at BPC.

    It implements the same "interface" as the Event model in the events app.
    It also adds the connection to BPC and a connection to a company in the jobs app.
    """

    bpcid = models.CharField(
        verbose_name="BPC-id",
        max_length=16,
        unique=True,
        blank=False,
        help_text=("Dette er id'en som blir brukt internt hos BPC. "
                   "Ikke endre den hvis du ikke vet hva du gjør."))
    company = models.ForeignKey(
        Company,
        verbose_name="Bedrift",
        blank=False,
        help_text="Hvilken bedrift som står bak bedriftspresentasjonen")

    class Meta:
        verbose_name = "bedriftspresentasjon"
        verbose_name_plural = "bedriftspresentasjoner"

    def get_registration_url(self):
        """Get the url used for registering for the event"""
        return reverse('bedpres_registration', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        """Get canonical url of object (used by django)"""
        return reverse("bedpres_detail", kwargs={'pk': self.pk, 'slug': self.slug})

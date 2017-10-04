from nablapps.events.models.abstract_event import AbstractEvent
from django.core.urlresolvers import reverse
from django.db import models

from nablapps.jobs.models import Company
from .bpcmixin import BPCEventMixin


class BedPres(BPCEventMixin, AbstractEvent):
    """
    Modell som lagrer informasjon om en bedpress fra BPC.
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

    def correct_picture(self):
        return self.picture if self.picture else self.company.picture

    def correct_cropping(self):
        return self.cropping if self.picture else self.company.cropping

    def get_registration_url(self):
        return reverse('bedpres_registration', kwargs={'pk': self.pk})

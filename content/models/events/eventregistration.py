# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.template import loader, Context
from django.core.urlresolvers import reverse

from .managers import RelatedEventRegistrationManager, EventRegistrationManager


class EventRegistration(models.Model):
    """Modell for påmelding på arrangementer.

    Inneholder både påmeldinger og venteliste.
    For ventelistepåmelding er attending satt til False og førstmann på ventelista har number=1.
    """

    event = models.ForeignKey(
        'Event',
        blank=False,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='bruker',
        blank=False,
        null=True)
    date = models.DateTimeField(
        verbose_name="Påmeldingsdato",
        auto_now_add=True,
        null=True)
    number = models.PositiveIntegerField(
        verbose_name='kønummer',
        blank=True,
        null=True,
        help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.')
    attending = models.BooleanField(
        verbose_name='har plass',
        default=True,
        blank=False,
        null=False,
        help_text="Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.")

    class Meta:
        verbose_name = 'påmelding'
        verbose_name_plural = 'påmeldte'
        unique_together = (("event", "user"), ("number", "attending"))

    objects = EventRegistrationManager()

    def __unicode__(self):
        return u'%s, %s is %s, place: %s' % (self.event,
                                             self.user,
                                             "Attending" if self.attending else "Waiting",
                                             self.number)

    def delete(self, *args, **kwargs):
        super(EventRegistration, self).delete(*args, **kwargs)
        EventRegistration.objects.update_lists(self.event)

    @classmethod
    def get_manager_for(cls, event):
        """Henter en manager for en gitt event."""
        return RelatedEventRegistrationManager(event)

    @property
    def waiting(self):
        """Indikerer om det er en ventelisteplass."""
        return not self.attending

    def waiting_list_place(self):
        """Returnerer hvilken plass man har på ventelisten gitt at man er på ventelisten."""
        return self.number if self.waiting else None

    def set_attending_if_waiting(self):
        """Flytter en bruker fra ventelisten til påmeldte hvis ikke allerede påmeldt."""
        if not self.attending:
            self.number = self.event.users_attending()+1
            self.attending = True
            self.save()

    def set_attending_and_send_email(self):
        self.set_attending_if_waiting()
        self._send_moved_to_attending_email()

    def _send_moved_to_attending_email(self):
        if self.user.email:
            subject = u'Påmeldt %s' % self.event.headline
            template = loader.get_template("events/moved_to_attending_email.txt")
            message = template.render(Context({'event': self, 'name': self.user.get_full_name()}))
            self.user.email_user(subject, message)

    def get_registration_url(self):
        return reverse('registration', kwargs={'pk': self.pk})

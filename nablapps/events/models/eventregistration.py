"""
Model representing a registration to an event.
"""
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template import loader

from ..exceptions import UserAlreadyRegistered


class EventRegistration(models.Model):
    """Modell for påmelding på arrangementer.

    Inneholder både påmeldinger og venteliste.
    For ventelistepåmelding er attending satt til False.
    Førstmann på ventelista er den påmeldingen med lavest id.
    """

    event = models.ForeignKey("Event", on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="bruker",
        on_delete=models.CASCADE,
        blank=False,
        null=True,
    )
    date = models.DateTimeField(
        verbose_name="Påmeldingsdato", auto_now_add=True, null=True
    )
    attending = models.BooleanField(
        verbose_name="har plass",
        default=True,
        blank=False,
        null=False,
        help_text="Hvis denne er satt til sann har man en plass "
        "på arrangementet ellers er det en ventelisteplass.",
    )
    penalty = models.IntegerField(
        verbose_name="Prikk", blank=True, null=True, default=None
    )
    attendance_registration = models.DateTimeField(
        verbose_name="Første regisreringstidspunkt",
        blank=True,
        null=True,
        default=None,
        help_text="Hvis dette tidspunktet er satt er det gjort en regisrering på at brukeren har møtt opp",
    )

    class Meta:
        verbose_name = "påmelding"
        verbose_name_plural = "påmeldte"
        unique_together = (("event", "user"),)
        db_table = "content_eventregistration"

        # This is the order the waiting list will be consulted.
        # So don't change this without thinking.
        ordering = ("id",)

    def __str__(self):
        return f'{self.event}, {self.user} is {"Attending" if self.attending else "Waiting"}'

    def clean(self):
        valid_penalties = self.event.get_penalty_rule_dict().values()
        if self.penalty not in valid_penalties and self.penalty is not None:
            raise ValidationError("Penalty value is not valid for this event")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.event.move_waiting_to_attending()

    @property
    def waiting(self):
        """Indikerer om det er en ventelisteplass."""
        return not self.attending

    def waiting_list_place(self):
        """Returnerer hvilken plass man har på ventelisten gitt at man er på ventelisten."""
        regs = self.event.waiting_registrations
        return (
            next(i + 1 for i, reg in enumerate(regs) if reg == self)
            if self.waiting
            else None
        )

    def set_attending_and_send_email(self):
        """Change the registration to be attending and send an email to the user."""
        if not self.attending:
            self.attending = True
            self.save()
            self._send_moved_to_attending_email()

    def _send_moved_to_attending_email(self):
        if self.user.email:
            subject = f"Påmeldt {self.event.headline}"
            template = loader.get_template("events/moved_to_attending_email.txt")
            message = template.render(
                {"event": self.event, "name": self.user.get_full_name()}
            )
            self.user.email_user(subject, message)

    def register_user_attendance(self):
        if self.attendance_registration is not None:
            raise UserAlreadyRegistered(
                "Your attendance is already registered!", eventregistration=self
            )
        else:
            self.attendance_registration = datetime.now()
            # Her sjekker man at det ikke finnes prikkregistrering på påmeldingen fra før
            # Det kan også være en løsning at vi setter antall prikekr til maksimalt antall

            if self.event.get_is_started() and self.penalty is None:
                self.penalty = self.event.get_late_penalty()
            else:
                self.penalty = self.event.get_show_penalty()
            self.full_clean()
            self.save()

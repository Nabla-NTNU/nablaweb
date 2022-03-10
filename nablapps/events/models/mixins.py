"""
Mixins to be inherited by AbstractEvent

They are split up in order make them easier to read,
and because there was (once upon a time) an idea to split up the information
about an event and the registration info into different models.
"""
from datetime import datetime

from django.db import models

from six.moves.urllib.parse import urlparse

from nablapps.accounts.models import FysmatClass

from ..exceptions import (
    RegistrationNotAllowed,
    RegistrationNotOpen,
    RegistrationNotRequiredException,
)


class EventInfoMixin(models.Model):
    """Abstract model defining info about an event, excluding registration info"""

    short_name = models.CharField(
        verbose_name="kort navn",
        max_length=20,
        blank=True,
        null=True,
        help_text="Brukes på steder hvor det ikke er plass til å skrive hele overskriften, "
        "for eksempel kalenderen.",
    )
    organizer = models.CharField(
        verbose_name="organisert av",
        max_length=100,
        blank=True,
        help_text="Den som står bak arrangementet",
    )
    location = models.CharField(verbose_name="sted", max_length=100, blank=False)
    event_start = models.DateTimeField(verbose_name="start", null=True, blank=False)
    event_end = models.DateTimeField(verbose_name="slutt", null=True, blank=True)
    facebook_url = models.CharField(
        verbose_name="facebook-url",
        blank=True,
        max_length=100,
        help_text="URL-en til det tilsvarende arrangementet på Facebook",
    )

    class Meta:
        abstract = True

    def has_started(self):
        """Has the event started?"""
        return self.event_start < datetime.now()

    def has_finished(self):
        """Is the event finished?"""
        return self.event_end and self.event_end < datetime.now()

    def has_enddate(self):
        return self.event_end is not None

    def clean(self):
        self.clean_facebook_url()
        super().clean()

    def clean_facebook_url(self):
        """Verifiserer formen på facebook-urlen, og endrer den hvis den er feil."""
        parsed = urlparse(self.facebook_url)
        noscheme = parsed.netloc + parsed.path
        self.facebook_url = (
            "http" + "://" + noscheme.replace("http://", "").replace("https://", "")
        )

        if self.facebook_url == "http://":
            self.facebook_url = ""


class RegistrationInfoMixin(models.Model):
    """Abstract model containing info about the registration.

    Most of these fields don't make any sense unless registration_required is set.
    """

    registration_required = models.BooleanField(
        verbose_name="påmelding", default=False, null=False, blank=False
    )
    registration_deadline = models.DateTimeField(
        verbose_name="påmeldingsfrist", null=True, blank=True
    )
    registration_start = models.DateTimeField(
        verbose_name="påmelding åpner", null=True, blank=True
    )
    deregistration_deadline = models.DateTimeField(
        verbose_name="avmeldingsfrist", null=True, blank=True
    )
    places = models.PositiveIntegerField(
        verbose_name="antall plasser", null=True, blank=True
    )
    has_queue = models.BooleanField(
        verbose_name="har venteliste",
        null=True,
        blank=True,
        help_text=(
            "Om ventelisten er på, vil det være mulig å melde seg på "
            "selv om arrangementet er fullt. "
            "De som er i ventelisten vil automatisk bli påmeldt "
            "etter hvert som plasser blir ledige."
        ),
    )
    open_for = models.ManyToManyField(
        FysmatClass,
        verbose_name="Åpen for",
        blank=True,
        help_text=(
            "Hvilke grupper som får lov til å melde seg på arrangementet. "
            "Hvis ingen grupper er valgt er det åpent for alle."
        ),
    )

    class Meta:
        abstract = True

    def allowed_to_attend(self, user):
        """Indikerer om en bruker har lov til å melde seg på arrangementet"""
        return (not self.open_for.exists()) or self.open_for.filter(user=user).exists()

    def registration_has_started(self):
        """Return whether registration has started"""
        return self.registration_required and self.registration_start < datetime.now()

    def registration_open(self):
        """Return whether it is possible to register for the event"""
        return (
            self.registration_has_started()
            and datetime.now() < self.registration_deadline
        )

    def deregistration_closed(self):
        """Return whether the event is closed for deregistration."""
        return self.deregistration_deadline and (
            self.deregistration_deadline < datetime.now()
        )

    def user_penalty_limit(self, user):
        """Counts the users penalties this term, used in _asser_user_allowed_to_register"""

        MAX_PENALTY = 4  # This is the limit at which one is not allowed to register
        # user.get_penalties returns EventRegistrations where the user has penalties
        penalty_count = sum([reg.penalty for reg in user.get_penalties()])
        return False if penalty_count >= MAX_PENALTY else True

    def _assert_user_allowed_to_register(self, user):
        if not self.registration_required:
            raise RegistrationNotRequiredException(event=self, user=user)
        elif not self.registration_open():
            raise RegistrationNotOpen(event=self, user=user)
        elif not self.allowed_to_attend(user):
            raise RegistrationNotAllowed(
                "Arrangementet er ikke åpent for ditt kull.", event=self, user=user
            )
        elif not self.user_penalty_limit(user):
            raise RegistrationNotAllowed(
                "Du har for mange prikker!", event=self, user=user
            )

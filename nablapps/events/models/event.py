"""
The Event model
"""
import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.urls import reverse

from nablapps.core.models import TimeStamped, WithPicture
from nablapps.jobs.models import Company
from nablapps.news.models import TextContent

from ..exceptions import (
    DeregistrationClosed,
    EventFullException,
    RegistrationAlreadyExists,
)
from .eventregistration import EventRegistration
from .mixins import EventInfoMixin, ExtendedRegistrationInfoMixin


class Event(
    ExtendedRegistrationInfoMixin, EventInfoMixin, TimeStamped, TextContent, WithPicture
):
    """Arrangementer både med og uten påmelding.
    Dukker opp som nyheter på forsiden.
    """

    # Penalty_rules is a dict where key is an integer and value is
    # a tuple with the name of the rule as first element and
    # a dictionary with the rules as second element.
    # The dict with rules has name of action as key, for example 'Did not meet',
    # and number of penalty-points that action gives as value
    #
    # The reason for not using a dict, where the key obviously would be the index,
    # is to make it easier to add/remove rules.
    penalty_rules = {
        0: ("Ingen prikker", {}),
        1: ("Bedpres", {"Oppmøte": 0, "Oppmøte for seint": 1, "Ikke møtt opp": 2}),
        2: (
            "Arrangement med betaling",
            {"Betalt": 0, "Betalt etter purring": 1, "Ikke betalt": 4},
        ),
        3: ("Arrangement uten betaling", {"Møtt opp": 0, "Ikke møtt opp": 1}),
    }

    penalty = models.IntegerField(
        default=0,
        choices=zip(penalty_rules.keys(), [rule[0] for rule in penalty_rules.values()]),
        blank=True,
        null=True,
    )

    is_bedpres = models.BooleanField(default=False)

    # Company is required if is_bedpres is True, see clean()
    company = models.ForeignKey(
        Company,
        verbose_name="Bedrift",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Kun relevant for bedriftspresentasjoner.",
    )

    def clean(self):
        if self.is_bedpres and self.company is None:
            raise ValidationError("Company must be set when 'is_bedpres' is True!")
        if not self.is_bedpres and self.company is not None:
            raise ValidationError("Company should only be set for bedpres!")
        if self.has_registration:
            if self.penalty is None:
                raise ValidationError("Penalty must be set when registration is True")

    class Meta:
        verbose_name = "arrangement"
        verbose_name_plural = "arrangement"
        permissions = (("administer", "Can administer models"),)
        db_table = "content_event"

    def __str__(self):
        return "%s, %s" % (self.headline, self.event_start.strftime("%d.%m.%y"))

    def get_penalty_rule_name(self):
        """Returns the name of the penalty rule for the event"""
        return self.penalty_rules[self.penalty][0]

    def get_penalty_rule_dict(self):
        """Returns the penalty rule dict for the event"""
        return self.penalty_rules[self.penalty][1]

    def get_short_name(self):
        """Henter short_name hvis den finnes, og kutter av enden av headline hvis ikke."""
        return (
            self.short_name
            if self.short_name
            else (self.headline[0:18].capitalize() + "...")
        )

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk, "slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.move_waiting_to_attending()

    ##################
    ## Registration ##
    ##################
    @property
    def waiting_registrations(self, rule):
        return self.eventregistration_set.filter(attending=False, rule=rule)

    @property
    def attending_registrations(self, rule):
        return self.eventregistration_set.filter(attending=True, rule=rule)

    def free_places(self):
        """Returnerer antall ledige plasser.

        dvs antall plasser som umiddelbart gir brukeren en garantert plass, og ikke bare
        ventelisteplass.
        Returnerer 0 hvis self.places er None.
        """
        try:
            return max(self.places - self.users_attending(), 0)
        except TypeError:
            return 0

    def is_full(self):
        """Return whether all places in the event are occupied"""
        return self.free_places() == 0

    def users_attending(self):
        """Returnerer antall brukere som er påmeldt."""
        return self.attending_registrations.count()

    def users_attending_emails(self):
        """
        :return: List of attending users emails.
        """
        attending = self.attending_registrations
        return [att.user.email for att in attending]

    def users_waiting(self):
        """Returnerer antall brukere som står på venteliste."""
        return self.waiting_registrations.count()

    def percent_full(self):
        """Returnerer hvor mange prosent av plassene som er tatt."""
        try:
            return min(self.users_attending() * 100 / int(self.places), 100)
        except TypeError:
            return 0
        except ZeroDivisionError:
            return 100

    def has_registration(self):
        return self.registration_info_collection.exists()

    def is_registered(self, user):
        return self.eventregistration_set.filter(user=user).exists()

    def is_attending(self, user):
        return self.attending_registrations.filter(user=user).exists()

    def is_waiting(self, user):
        return self.waiting_registrations.filter(user=user).exists()

    def get_attendance_list(self):
        return [e.user for e in self.attending_registrations]

    def get_waiting_list(self):
        return [e.user for e in self.waiting_registrations]

    def has_rule_for_user(self, user):
        """Return true if theere exists a rule for the user."""
        try:
            user_fysmat_class = FysmatClass.objects.get(user=user)
        except FysmatClass.DoesNotExist:
            # Oh no, user does not have a FysmatClass!
            pass
        except FysmatClass.MultipleObejctsReturned:
            # OH Oh no, user has multiple FysmatClasses!
            pass

        try:
        except RegistrationInfo.DoesNotExist:
            # This should be expected to happen sometimes, so should handle this well
            pass
        except RegistrationInfo.MultipleObjectsReturned:
            pass

    def get_rule_for_user(self, user):
        """Get the registration info rule under which the user should be registered.
        """
        try:
            user_fysmat_class = FysmatClass.objects.get(user=user)
        except FysmatClass.DoesNotExist:
            # Oh no, user does not have a FysmatClass!
            raise FysmatClass.DoesNotExist
        except FysmatClass.MultipleObejctsReturned:
            # OH Oh no, user has multiple FysmatClasses!
            raise FysmatClass.MultipleObjecstReturned

        try:
            rule = self.registration_info_collection.get(open_for=user_fysmat_class)
        except RegistrationInfo.DoesNotExist:
            # This should be expected to happen sometimes, so should handle this well
            raise RegistrationInfo.DoesNotExist
        except RegistrationInfo.MultipleObjectsReturned:
            raise RegistrationInfo.MultipleObjectsReturned

        return rule

    def register_user(self, user, ignore_restrictions=False):
        """
        Tries to register a user for an event.

        If the user is not allowed to attend, an exception will be thrown.
        Set ignore_restrictions to True to register a user anyways.
        """
        if not ignore_restrictions:
            self._assert_user_allowed_to_register(user)

        registration = EventRegistration(
            event=self, rule=self.get_rule_for_user(user), user=user,
        )

        if not self.is_full() or ignore_restrictions:
            registration.attending = True
        elif self.has_queue:
            registration.attending = False
        else:
            raise EventFullException(event=self, user=user)
        try:
            registration.save()
        except IntegrityError:
            raise RegistrationAlreadyExists(event=self, user=user)
        return registration

    def deregister_user(self, user, respect_closed=True):
        """
        Melder brukeren av arrangementet.
        respect_closed gir mulighet til å avmelde brukere etter avmeldingsfrist,
        fra administrative verktøy
        """
        regs = self.eventregistration_set
        if self.deregistration_closed() and respect_closed:
            raise DeregistrationClosed(event=self, user=user)
        try:
            reg = regs.get(user=user)
            reg.delete()
        except EventRegistration.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.info("Attempt to deregister user from non-existent event.")

    def move_waiting_to_attending(self):
        """
        Moves as many as there are free places left on the event.
        """
        free_places = self.free_places()
        waiting_regs = self.waiting_registrations[:free_places]
        for reg in waiting_regs:
            reg.set_attending_and_send_email()

    def get_registration_url(self):
        return reverse("registration", kwargs={"pk": self.pk})


def attending_events(user, today):
    """Get the future events attended by a user"""
    if user.is_anonymous:
        return []
    regs = user.eventregistration_set.filter(event__event_start__gte=today)
    events = []
    for reg in regs:
        event = reg.event
        event.attending = reg.attending
        event.waiting = not reg.attending
        events.append(event)
    return events

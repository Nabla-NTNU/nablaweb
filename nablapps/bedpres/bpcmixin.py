"""
BPC integration code

Uses the bpc_client package.
"""
import logging
from django.utils.functional import cached_property

from bpc_client import BPCEvent
from bpc_client.exceptions import BPCResponseException, BPCConnectionError

from nablapps.accounts.models import NablaUser as User
from nablapps.events.exceptions import (
    EventFullException,
    RegistrationAlreadyExists,
    RegistrationNotOpen,
    EventException,
)
from .utils import get_bpc_user_dictionary


class RegistrationInfo: # pylint: disable=too-few-public-methods
    """
    A simple class used for the return value of register_user.

    Emulates the EventRegistration
    """

    def __init__(self, attending):
        self.attending = attending
        self.waiting = not attending


class WrongClass(Exception):
    """Exception to be thrown when a BPC says that a user is in a wrong class."""
    def __init__(self, event, user):
        super().__init__()
        self.user = user
        self.event = event


class BPCEventMixin:
    """Mixin-class to add the same methods for registration as the Event-model from content."""
    bpcid = None

    # Dummy data in case of no connection with BPC
    _dummy_data = {
        "max_year": "10",
        "min_year": "10",
        "open_for": "10",
        "seats": "0",
        "seats_available": "0",
        "this_attending": "0",
    }

    @cached_property
    def bpc_event(self):
        """
        Get the bpc_event object from the bpc_client package.

        This will only be cached and thus only downloaded once for each Bedpres.
        """
        event = BPCEvent(bpc_id=self.bpcid)
        try:
            event.update_data()
        except BPCConnectionError:
            event.data = self._dummy_data
            logger = logging.getLogger(__name__)
            logger.error("No connection to BPC. Used dummy data instead.")
        except BPCResponseException as e:
            if e.bpc_error_code == '403' or e.bpc_error_code == '103':
                event.data = self._dummy_data
                logger = logging.getLogger(__name__)
                logger.error("BPC doesn't have an event with id %d. "
                             "Used dummy data instead.", self.bpcid)
            else:
                raise e
        return event

    def register_user(self, user):
        """
        Try to register a user

        return: RegistrationInfo indicating if the user is attending
                or is on the waiting list.
        raises EventException
        """
        try:
            user_dict = get_bpc_user_dictionary(user)
            is_attending = self.bpc_event.add_attending(**user_dict)
            return RegistrationInfo(is_attending)
        except BPCResponseException as e:
            if e.bpc_error_code == "402":
                raise EventFullException(event=self, user=user)
            elif e.bpc_error_code == "405":
                raise RegistrationAlreadyExists(event=self, user=user)
            elif e.bpc_error_code in ("408", "409"):
                raise RegistrationNotOpen(event=self, user=user)
            elif e.bpc_error_code in ("401", "410"):
                raise WrongClass(event=self, user=user)
            raise e

    def deregister_user(self, user):
        """Remove user from attending list or waiting list"""
        self.bpc_event.rem_attending(username=user.username)

    def get_attendance_list(self):
        """Get queryset of locale users in the attending list"""
        return User.objects.filter(username__in=self.attending_usernames)

    def get_waiting_list(self):
        """Get queryset of locale users in the waiting list"""
        return User.objects.filter(username__in=self.waiting_usernames)

    @property
    def attending_usernames(self):
        """Get a list of usernames in the attending list"""
        try:
            return self.bpc_event.attending_usernames
        except BPCConnectionError:
            return []
        except BPCResponseException as e:
            raise EventException(e)

    @property
    def waiting_usernames(self):
        """Get a list of usernames in the waiting list"""
        try:
            return self.bpc_event.waiting_usernames
        except BPCConnectionError:
            return []
        except BPCResponseException as e:
            raise EventException(e)

    def is_registered(self, user):
        """Check if the user is either attending or in the waiting list"""
        return self.is_attending(user) or self.is_waiting(user)

    def is_attending(self, user):
        """Check if user is in the attending list"""
        return user.username in self.attending_usernames

    def is_waiting(self, user):
        """Check if user is in waiting list"""
        return user.username in self.waiting_usernames

    def free_places(self):
        """Return number of remaining places"""
        return self.bpc_event.seats_available

    def is_full(self):
        """Indicates whether all the places are taken"""
        return self.free_places() == 0

    def users_attending(self):
        """Number of people that are attending"""
        return self.bpc_event.this_attending

    def users_waiting(self):
        """Number of people in the waiting list"""
        return len(self.waiting_usernames)

    def percent_full(self):
        """Percentage of places that reserved for some people"""
        places = self.bpc_event.seats
        return ((places - self.free_places()) * 100) / places if places != 0 else 100

    def open_for_classes(self):
        """Return a string representing the classes that are allowed to attend"""
        min_year = self.bpc_event.min_year
        max_year = self.bpc_event.max_year
        if max_year == '99':
            max_year = ''
        if min_year == max_year:
            return min_year
        return min_year + '-' + max_year


class BedpresNoModel(BPCEventMixin):
    """Concrete class that is not actually a model"""
    def __init__(self, bpcid):
        self.bpcid = bpcid

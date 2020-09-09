"""
Exceptions for events app

To have so many exception types might be a little over the top, but ...
"""


class EventException(Exception):
    """Base exception type for events app"""


class UserRegistrationException(EventException):
    """Base class for exceptions that can be raised when a user trys to register for an event"""

    def __init__(self, *args, event=None, user=None):
        super().__init__(*args)
        self.event = event
        self.user = user


class RegistrationNotRequiredException(UserRegistrationException):
    """Raised when a user tries to register to an event without registration"""


class RegistrationNotOpen(UserRegistrationException):
    """Raised when a user tries to register to and that is not open for registration"""


class RegistrationAlreadyExists(UserRegistrationException):
    """Raised if user already registered to the event"""


class RegistrationNotAllowed(UserRegistrationException):
    """Raised if the user is not allowed to register to an event"""


class EventFullException(UserRegistrationException):
    """Raised if all places are taken on an event"""


class DeregistrationClosed(UserRegistrationException):
    """Raised when a user tries to deregister from an event after the deregistration deadline"""


class UserAttendanceException(EventException):
    """Base class for exceptions that can be raised when a user trys to register for an event"""

    def __init__(
        self,
        *args,
        eventregistration=None,
        user=None,
        identification_string=None,
        method=None
    ):
        super().__init__(*args)
        self.eventregistration = eventregistration
        self.identification_string = identification_string
        self.method = None


class EventNotStartedException(EventException):
    """Raised when a user tries to start an event before event has started"""


class UserNotAttending(UserAttendanceException):
    """Raised whten the user is on the waiting list"""


class UserAlreadyRegistered(UserAttendanceException):
    """Raised when users attendance already has been registered"""


class UserNotPaid(UserAttendanceException):
    """Raised when the user has not paid for their ticket. This exception is not used but might be used in the future"""

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

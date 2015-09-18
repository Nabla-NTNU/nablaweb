

class EventException(Exception):
    pass


class UserRegistrationException(EventException):
    token = None

    def __init__(self, event=None, user=None):
        self.event = event
        self.user = user


class RegistrationNotRequiredException(UserRegistrationException):
    token = "noreg"


class RegistrationNotOpen(UserRegistrationException):
    token = "not_open"


class RegistrationAlreadyExists(UserRegistrationException):
    token = "reg_exists"


class RegistrationNotAllowed(UserRegistrationException):
    token = "not_allowed"


class EventFullException(UserRegistrationException):
    token = "full"


class DeregistrationClosed(UserRegistrationException):
    token = "dereg_closed"

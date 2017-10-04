

class EventException(Exception):
    pass


class UserRegistrationException(EventException):
    token = None

    def __init__(self, event=None, user=None):
        self.event = event
        self.user = user


class RegistrationNotRequiredException(UserRegistrationException):
    pass


class RegistrationNotOpen(UserRegistrationException):
    pass


class RegistrationAlreadyExists(UserRegistrationException):
    pass


class RegistrationNotAllowed(UserRegistrationException):
    pass


class EventFullException(UserRegistrationException):
    pass


class DeregistrationClosed(UserRegistrationException):
    pass

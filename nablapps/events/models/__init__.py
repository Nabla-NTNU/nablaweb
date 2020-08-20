"""
Models for event app
"""
from .event import Event
from .eventregistration import EventRegistration
from .mixins import RegistrationInfo

__all__ = ["Event", "EventRegistration", "RegistrationInfo"]

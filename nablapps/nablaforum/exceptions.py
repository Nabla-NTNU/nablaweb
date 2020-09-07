"""
Exceptions for forum
"""


class ForumException(Exception):
    """Base exception"""


class ThreadCreationException(ForumException):
    """
    Raised when creation of a new forum thread fails.
    """


class MessageCreationException(ForumException):
    """
    Raised when creation of a new forum message fails.
    """


class ChannelCreationException(ForumException):
    """
    Raised when creation of a new forum channel fails.
    """

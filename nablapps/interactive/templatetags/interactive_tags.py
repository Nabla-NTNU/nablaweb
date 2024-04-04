"""
Tags for interactive
"""

from django import template

from ..models.place import time_of_last_action

register = template.Library()


@register.filter
def timestamp_of_last_action(user, grid):
    """
    Template filter implementing `time_of_last_action` from
    models/place.py.
    """
    if not user.is_authenticated:
        return 0
    return time_of_last_action(user, grid).timestamp()

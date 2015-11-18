from django.db import models
from content.models.mixins import EditableMedia
from accounts.models import NablaUser


class InteractiveElement(EditableMedia, models.Model):
    """
    Model for an element requiring user interaction.
    """

    template = models.CharField(
        max_length=100,
        verbose_name="Template",
        default="interactive/advent_door_base.html"
    )

    class Meta:
        abstract = True


class Scoreboard(models.Model):
    """
    Represents a score board for a given element.
    """

    element = None
    
    class Meta:
        abstract = True
 

class InteractionResult(models.Model):
    """
    Represents an interaction with a given element. For example a score.
    """

    when = models.DateTimeField(
        auto_created=True
    )

    class Meta:
        abstract = True

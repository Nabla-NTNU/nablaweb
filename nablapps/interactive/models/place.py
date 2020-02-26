from datetime import datetime

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver

from nablapps.accounts.models import NablaUser

DEFAULT_COLOR = "FFFFFF"


class PlaceGrid(models.Model):

    width = models.PositiveIntegerField(
        verbose_name="Bredde", validators=[MinValueValidator(1)]
    )

    height = models.PositiveIntegerField(
        verbose_name="Høyde", validators=[MinValueValidator(1)]
    )

    # Cooldown in seconds
    cooldown = models.PositiveIntegerField(verbose_name="Cooldown (s)")

    enabled = models.BooleanField(default=True)

    publish_date = models.DateTimeField(verbose_name="Slippdato",)

    created = models.DateTimeField(auto_now_add=True)

    # Set in `create_grid`
    last_updated = models.DateTimeField(blank=True, null=True)

    legal_colors = [
        "FFFFFF",
        "E4E4E4",
        "888888",
        "222222",
        "FFA7D1",
        "CF6EE4",
        "820080",
        "E50000",
        "E5D900",
        "E59500",
        "94E044",
        "02BE01",
        "A06A42",
        "00D3DD",
        "0083C7",
        "0000EA",
    ]

    @property
    def is_published(self):
        if settings.DEBUG:
            return True
        return datetime.now() >= self.publish_date

    def __str__(self):
        return (
            f"Grid [{self.pk}] ({self.height}x{self.width}) "
            f"{'enabled' if self.enabled else ''} "
            f"{'published' if self.is_published else ''}"
        )


@receiver(models.signals.post_save, sender=PlaceGrid)
def create_grid(sender, instance, created, **kwargs):
    # Create the corresponing lines and pixels when the grid is created
    if created:
        # Assumes system time is in UTC
        now = datetime.now()
        instance.last_updated = now
        instance.save()
        for y in range(instance.height):  # Create lines
            line = PlaceLine.objects.create(y=y, grid=instance, last_updated=now)
            for x in range(instance.width):  # Create pixels
                PlacePixel.objects.create(
                    x=x, color=DEFAULT_COLOR, line=line, last_updated=now
                )


class PlaceLine(models.Model):
    y = models.PositiveIntegerField()  # y-value from 0 to PlaceGrid.height -1

    grid = models.ForeignKey(PlaceGrid, related_name="lines", on_delete=models.CASCADE)

    last_updated = models.DateTimeField()


class PlacePixel(models.Model):
    x = models.PositiveIntegerField()  # x-value from 0 to PlaceGrid.width -1

    color = models.CharField(verbose_name="Color", max_length=6)

    line = models.ForeignKey(PlaceLine, related_name="pixels", on_delete=models.CASCADE)

    latest_action = models.OneToOneField(
        "PlaceAction",
        null=True,
        blank=True,
        related_name="pixel",
        on_delete=models.CASCADE,
    )

    last_updated = models.DateTimeField()


class PlaceAction(models.Model):
    user = models.ForeignKey(
        NablaUser, related_name="actions", on_delete=models.CASCADE
    )
    grid = models.ForeignKey(
        PlaceGrid, related_name="actions", on_delete=models.CASCADE
    )
    time = models.DateTimeField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    color = models.CharField(max_length=6)


def extract_action(action):
    """Return a dict containing the relevant fields of a `PlaceAction`"""
    return {
        "x": action.x,
        "y": action.y,
        "color": action.color,
        "time": action.time.timestamp(),  # Unix timestamp
        "username": action.user.username,
    }


def get_pixel_data(pixel):
    """Return a dict containing relevant information about the pixel"""
    if pixel.latest_action is None:
        return {"color": DEFAULT_COLOR, "time": 0, "username": ""}
    else:
        action = pixel.latest_action
        return {
            "color": action.color,
            "time": action.time.timestamp(),  # Unix timestamp
            "username": action.user.username,
        }


def time_of_last_action(user, grid):
    """
    Return a datetime representing the time when the user last
    submitted a pixel to that grid.
    Returns datetime(1970,1,1,1) (0 timestamp) if the user has no actions.
    """
    try:
        latest_action = user.actions.filter(grid=grid).latest("time")
    except PlaceAction.DoesNotExist:
        time = datetime(1970, 1, 1, 1)
    else:
        time = latest_action.time
    return time

"""
Defines and registers django signal receivers
"""

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import FrontPageNews


@receiver(pre_delete)
def callback(sender, instance, **kwargs):  # pylint: disable=W0613
    """
    Delete front-page-items corresponding to a deleted object

    Unless this is done, there will be things on the front-page not corresponding to
    an existing object.
    """
    if not hasattr(instance, "id"):
        return

    FrontPageNews.objects.filter(
        object_id=instance.id,
        content_type=ContentType.objects.get_for_model(instance.__class__),
    ).delete()

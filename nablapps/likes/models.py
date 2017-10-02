from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class LikePressManager(models.Manager):

    @staticmethod
    def _get_kwargs(instance, user):
        d = LikePressManager._get_object_kwargs(instance)
        d['user'] = user
        return d

    @staticmethod
    def _get_object_kwargs(instance):
        return {
            'content_type': ContentType.objects.get_for_model(instance.__class__),
            'object_id': instance.id
        }

    def toggle(self, instance, user):
        """Creates or deletes a like press

        returns whether it created a like.
        """
        obj, created = self.get_or_create(**self._get_kwargs(instance, user))
        if not created:
            obj.delete()
        return created

    def like_exists(self, instance, user):
        return self.filter(**self._get_kwargs(instance, user)).exists()

    def like_count(self, instance):
        return self.filter(**self._get_object_kwargs(instance)).count()


class LikePress(models.Model):
    """
    Represents a like click on some object.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="like_presses")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikePressManager()

    class Meta:
        unique_together = (('user', 'content_type', 'object_id'),)

    def __str__(self):
        return "{self.user} likes '{self.content_object}'".format(self=self)


toggle_like = LikePress.objects.toggle
user_likes = LikePress.objects.like_exists
get_like_count = LikePress.objects.like_count

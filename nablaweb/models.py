from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.fields import GenericForeignKey, ContentType


class GeneralOptions(models.Model):

    favicon = models.ImageField(
        blank=True
    )

    site = models.OneToOneField(
        Site
    )

    main_story_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True    
    )

    main_story_id = models.PositiveIntegerField(
        null=True
    )

    main_story = GenericForeignKey(
        'main_story_content_type',
        'main_story_id'
    )

    @staticmethod
    def get_current():
        try:
            return GeneralOptions.objects.get(site=Site.objects.get_current())
        except GeneralOptions.DoesNotExist:
            return GeneralOptions.objects.create(site=Site.objects.get_current())
    


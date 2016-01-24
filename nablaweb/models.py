from django.db import models
from django.contrib.sites.models import Site


class GeneralOptions(models.Model):

    favicon = models.ImageField(
        blank=True
    )

    site = models.OneToOneField(
        Site
    )

    @staticmethod
    def get_current():
        return GeneralOptions.objects.get(site=Site.get_current())
    


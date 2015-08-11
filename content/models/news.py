# -*- coding: utf-8 -*-


from django.db import models

from content.models import Content


class News(Content):

    # Tekstinnhold
    headline = models.CharField(
        verbose_name="tittel",
        max_length=100,
        blank=False)
    lead_paragraph = models.TextField(
        verbose_name="ingress",
        blank=True,
        help_text="Vises på forsiden og i artikkelen")
    body = models.TextField(
        verbose_name="brødtekst",
        blank=True,
        help_text=(
            "Vises kun i artikkelen. "
            "Man kan her bruke <a href=\"http://en.wikipedia.org/wiki/Markdown\" target=\"_blank\">"
            "markdown</a> for å formatere teksten."))

    PRIORITY_NUMBERS = (
        (0, '0 - Dukker ikke opp'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10 - Er på forsida hele tiden')
        )
    priority = models.IntegerField(
        verbose_name="Prioritering",
        choices=PRIORITY_NUMBERS,
        default=5,
        blank=False,
        null=False,
        help_text=(
            "Prioritering av saken på forsiden. "
            "Dette fungerer for øyeblikket ikke. "
            "Bortsett fra at prioritering=0 fjerner saken fra forsiden."))

    class Meta:
        verbose_name = "nyhet"
        verbose_name_plural = "nyheter"

    def correct_picture(self):
        return self.picture

    def correct_cropping(self):
        return self.cropping

    @property
    def as_child_class(self):
        if hasattr(self, 'advert'):
            return self.advert
        elif hasattr(self, 'bedpres'):
            return self.bedpres
        else:
            return self

    def __str__(self):
        return self.headline

    def __unicode__(self):
        return self.headline

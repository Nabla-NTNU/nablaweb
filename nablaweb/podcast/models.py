# -*- coding: utf-8 -*-

from django.db import models
from image_cropping.fields import ImageRatioField


class Podcast(models.Model):

    # Bildeopplasting med resizing og cropping
    image = models.ImageField(
        upload_to="news_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text="Bilder som er større enn 300x300 px ser best ut. Du kan beskjære bildet etter opplasting.")
    cropping = ImageRatioField(
        'image',
        '300x300',
        allow_fullsize=False,
        verbose_name="Beskjæring",
        help_text="Bildet vises i full form på detaljsiden."
    )

    title = models.CharField(
        verbose_name='tittel',
        max_length=200,
        blank=False
    )
    description = models.TextField(
        verbose_name='beskrivelse',
        help_text='Tekst. Man kan her bruke <a href="http://en.wikipedis.org/wiki/Markdown\"target=\"_blank\">markdown</a> for å formatere teksten.',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='publisert',
        auto_now_add=True,
        blank=False,
        null=True,
        editable=False,
    )
    file = models.FileField(
        upload_to='podcast',
        blank=False,
        verbose_name='lydfil',
        help_text='Filformat: MP3'
    )

    view_counter = models.IntegerField(
        editable=False,
        default=0
    )

    def addView(self):
        self.view_counter += 1
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcast'
        ordering = ["-pub_date"]

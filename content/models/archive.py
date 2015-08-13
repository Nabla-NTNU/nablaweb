# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse


class Archive(models.Model):
    name = models.CharField(
        max_length=80,
        blank=False,
        verbose_name="Navn",
    )

    entries = models.ManyToManyField(
        'ArchiveEntry',
        verbose_name="Innlegg",
        blank=True,
        related_name='entries'
    )

    description = models.TextField(
        verbose_name="Beskrivelse",
        blank=True
    )


class ArchiveEntry(models.Model):
    archive = models.ForeignKey(
        'Archive',
        verbose_name='Arkiv',
        related_name='archive'
    )

    title = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Tittel"
    )

    pub_date = models.DateField(
        verbose_name='publisert',
        blank=False,
        null=True,
        help_text="Publikasjonsdato"
    )

    file = models.FileField(
        upload_to='archive',
        verbose_name='Fil',
        help_text="Filnavn"
    )

    class Meta:
        verbose_name = 'Arkivinnlegg'
        verbose_name_plural = 'Arkivinnlegg'
        ordering = ("-pub_date",)

    def get_absolute_url(self):
        return reverse('archive_entry', kwargs={'archive': self.archive.name})

    def __str__(self):
        return self.headline

    def __unicode__(self):
        return self.headline

# -*- coding: utf-8 -*-

from django.db import models
from content.models import News


class MeetingRecord(News):
    pub_date = models.DateField(
        verbose_name='publisert',
        blank=False,
        null=True,
        help_text="Publikasjonsdato")
    file = models.FileField(
        upload_to='meeting_records',
        verbose_name='PDF-fil',
        null=True,
        blank=False,
        help_text="Filnavn")

    class Meta:
        verbose_name = 'Møtereferat'
        verbose_name_plural = 'Møtereferater'

    def __str__(self):
        return self.headline

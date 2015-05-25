# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0003_auto_20150521_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '770x300', free_crop=False, help_text=None, hide_image_field=False, verbose_name='Beskjæring', adapt_rotation=False, size_warning=False, allow_fullsize=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='podcast',
            name='image',
            field=models.ImageField(upload_to='news_pictures', null=True, help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.', blank=True, verbose_name='Bilde'),
            preserve_default=True,
        ),
    ]

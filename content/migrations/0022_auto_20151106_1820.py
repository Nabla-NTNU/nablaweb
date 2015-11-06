# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('content', '0021_auto_20151106_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='allow_comments',
            field=models.BooleanField(default=True, verbose_name='Tillat kommentarer', help_text='Hvorvidt kommentering er tillatt'),
        ),
        migrations.AddField(
            model_name='news',
            name='content_type',
            field=models.ForeignKey(null=True, editable=False, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='news',
            name='picture',
            field=models.ImageField(null=True, blank=True, verbose_name='Bilde', upload_to='uploads/news_pictures', help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('jobs', '0011_auto_20151106_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='allow_comments',
            field=models.BooleanField(verbose_name='Tillat kommentarer', default=True, help_text='Hvorvidt kommentering er tillatt'),
        ),
        migrations.AddField(
            model_name='company',
            name='content_type',
            field=models.ForeignKey(editable=False, null=True, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='company',
            name='picture',
            field=models.ImageField(blank=True, verbose_name='Bilde', null=True, upload_to='uploads/news_pictures', help_text='Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.'),
        ),
    ]

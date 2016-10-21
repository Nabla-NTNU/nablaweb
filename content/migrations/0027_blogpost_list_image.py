# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_albumimage_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='list_image',
            field=models.ImageField(verbose_name='Listebilde', upload_to='blogpics', help_text='Her kan du legge til bilde som vises i listevisningen av bloggene', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0027_blogpost_list_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='list_image',
            field=models.ImageField(upload_to='blogpics', verbose_name='Listebilde', help_text='Bilde som vises i listevisningen av bloggene', blank=True, null=True),
        ),
    ]

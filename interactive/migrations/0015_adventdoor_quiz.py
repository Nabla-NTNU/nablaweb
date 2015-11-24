# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0014_adventdoor_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='quiz',
            field=models.ForeignKey(verbose_name='Lenket quiz', blank=True, to='interactive.Quiz', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0021_auto_20161118_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='user_test',
            field=models.ForeignKey(to='interactive.Test', verbose_name='Lenket brukertest', blank=True, null=True),
        ),
    ]

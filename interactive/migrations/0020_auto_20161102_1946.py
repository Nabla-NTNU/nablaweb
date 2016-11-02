# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0019_auto_20160402_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventdoor',
            name='number',
            field=models.IntegerField(verbose_name='Nummer'),
        ),
        migrations.AlterUniqueTogether(
            name='adventdoor',
            unique_together=set([('number', 'calendar')]),
        ),
    ]

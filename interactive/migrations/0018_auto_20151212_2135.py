# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0017_auto_20151210_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='question',
            field=models.TextField(verbose_name='Spørsmål'),
        ),
    ]

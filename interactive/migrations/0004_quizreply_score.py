# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0003_quizreply_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizreply',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

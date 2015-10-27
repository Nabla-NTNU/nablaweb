# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0004_quizreply_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='is_lottery',
            field=models.BooleanField(verbose_name='Har trekning', default=False),
        ),
    ]

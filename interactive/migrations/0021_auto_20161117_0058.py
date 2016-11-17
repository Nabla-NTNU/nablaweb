# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0020_auto_20161102_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='test',
            name='results',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='alternatives',
        ),
        migrations.AddField(
            model_name='testquestion',
            name='test',
            field=models.ForeignKey(default=None, related_name='questions', to='interactive.Test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testquestionalternative',
            name='question',
            field=models.ForeignKey(default=None, related_name='alternatives', to='interactive.TestQuestion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testresult',
            name='test',
            field=models.ForeignKey(default=None, related_name='results', to='interactive.Test'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nablaweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='generaloptions',
            name='main_story_content_type',
            field=models.ForeignKey(null=True, to='contenttypes.ContentType', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='generaloptions',
            name='main_story_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]

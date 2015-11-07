# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('podcast', '0013_podcast_allow_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='content_type',
            field=models.ForeignKey(editable=False, null=True, to='contenttypes.ContentType'),
        ),
    ]

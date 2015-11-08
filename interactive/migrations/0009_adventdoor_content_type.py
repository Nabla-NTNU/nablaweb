# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('interactive', '0008_auto_20151104_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='content_type',
            field=models.ForeignKey(editable=False, null=True, to='contenttypes.ContentType'),
        ),
    ]

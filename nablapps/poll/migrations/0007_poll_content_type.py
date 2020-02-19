# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("poll", "0006_auto_20150926_1409"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="content_type",
            field=models.ForeignKey(
                to="contenttypes.ContentType",
                editable=False,
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
    ]

# -*- coding: utf-8 -*-
# Adds created field.
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("officeBeer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="depositrequest",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]

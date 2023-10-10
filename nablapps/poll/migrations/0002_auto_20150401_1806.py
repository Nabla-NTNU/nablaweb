# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("poll", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="added_by",
            field=models.CharField(
                verbose_name="Lagt til av",
                max_length=100,
                help_text="Hvem som la til valget i avstemningen",
            ),
        ),
    ]

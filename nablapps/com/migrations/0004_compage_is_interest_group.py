# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("com", "0003_auto_20151007_1436"),
    ]

    operations = [
        migrations.AddField(
            model_name="compage",
            name="is_interest_group",
            field=models.BooleanField(
                verbose_name="Interessegruppe",
                help_text="Er ikke fullverdig komité",
                default=True,
            ),
        ),
    ]

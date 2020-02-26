# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0005_auto_20150926_0938"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="poll",
            options={
                "verbose_name": "Avstemning",
                "verbose_name_plural": "Avstemninger",
            },
        ),
    ]

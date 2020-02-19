# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0003_auto_20150925_2315"),
    ]

    operations = [
        migrations.AddField(
            model_name="poll",
            name="is_user_poll",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="Er brukerpoll"
            ),
        ),
    ]

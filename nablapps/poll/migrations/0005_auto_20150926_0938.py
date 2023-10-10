# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("poll", "0004_poll_is_user_poll"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="poll",
            field=models.ForeignKey(
                related_name="choices", to="poll.Poll", on_delete=models.CASCADE
            ),
        ),
    ]

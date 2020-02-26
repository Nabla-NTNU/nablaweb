# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_move_to_new_likepress_app"),
    ]

    operations = [
        migrations.AddField(
            model_name="nablagroup",
            name="logo",
            field=models.FileField(
                blank=True, upload_to="logos", verbose_name="Logo", null=True
            ),
        ),
    ]

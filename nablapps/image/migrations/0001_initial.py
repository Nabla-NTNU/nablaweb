# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name="ContentImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        verbose_name="Bildefil", upload_to="uploads/content"
                    ),
                ),
            ],
            options={
                "verbose_name": "Innholdsbilde",
                "verbose_name_plural": "Innholdsbilder",
                "db_table": "content_contentimage",
            },
        ),
    ]

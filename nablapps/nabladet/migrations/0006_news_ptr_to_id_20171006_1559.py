# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nabladet", "0005_move_fields_from_news"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nablad",
            name="news_ptr",
            field=models.AutoField(
                auto_created=True,
                default=1,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.RenameField(model_name="nablad", old_name="news_ptr", new_name="id"),
    ]

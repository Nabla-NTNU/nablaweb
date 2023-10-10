# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import nablapps.exchange


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exchange",
            options={
                "verbose_name_plural": "utvekslinger",
                "ordering": ["student"],
                "verbose_name": "utveksling",
            },
        ),
        migrations.AlterModelOptions(
            name="info",
            options={"verbose_name_plural": "info", "verbose_name": "info"},
        ),
        migrations.AddField(
            model_name="info",
            name="file",
            field=models.FileField(
                null=True,
                validators=[nablapps.exchange.models.validate_file_extension],
                upload_to="utveksling",
                blank=True,
                help_text="PDF-fil. Hvis dette eksisterer vil ikke teksten ovenfor bli brukt.",
                verbose_name="PDF-fil",
            ),
        ),
        migrations.AddField(
            model_name="info",
            name="link",
            field=models.TextField(
                verbose_name="ekstern link",
                help_text="Link som kan brukes i stedet for pdf-fil eller tekst. Har høyest prioritet",
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="end",
            field=models.DateField(
                help_text="Dato utveksling sluttet. Kun måned som brukes."
            ),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="start",
            field=models.DateField(
                help_text="Dato utveksling startet. Kun måned som brukes."
            ),
        ),
    ]

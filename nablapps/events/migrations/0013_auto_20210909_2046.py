# Generated by Django 3.1.13 on 2021-09-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0012_auto_20201021_2154"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="has_queue",
            field=models.BooleanField(
                blank=True,
                help_text="Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.",
                null=True,
                verbose_name="har venteliste",
            ),
        ),
    ]

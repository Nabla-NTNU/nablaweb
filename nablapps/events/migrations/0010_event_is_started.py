# Generated by Django 3.0.7 on 2020-09-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0009_remove_event_has_started"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="is_started",
            field=models.BooleanField(default=False),
        ),
    ]

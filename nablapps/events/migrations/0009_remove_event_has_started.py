# Generated by Django 3.0.7 on 2020-09-04 18:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0008_event_has_started"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="has_started",
        ),
    ]

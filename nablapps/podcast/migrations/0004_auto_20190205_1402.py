# Generated by Django 2.1.5 on 2019-02-05 14:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("podcast", "0003_auto_20171026_1258"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="podcast",
            name="publication_date",
        ),
        migrations.RemoveField(
            model_name="podcast",
            name="published",
        ),
    ]

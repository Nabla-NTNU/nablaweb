# Generated by Django 3.1.14 on 2022-02-11 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vote", "0008_merge_20220211_0058"),
    ]

    operations = [
        migrations.AddField(
            model_name="votingevent",
            name="polling_period",
            field=models.IntegerField(default=2000, verbose_name="Polling interval"),
        ),
    ]

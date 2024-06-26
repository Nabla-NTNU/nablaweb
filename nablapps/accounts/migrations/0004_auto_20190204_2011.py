# Generated by Django 2.1.5 on 2019-02-04 20:11

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_merge_20190123_2039"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="fysmatclass",
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="nablagroup",
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterField(
            model_name="nablauser",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        ),
    ]

# Generated by Django 2.1.13 on 2019-10-25 21:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("nablaforum", "0002_add_created_datetime"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="channel",
            name="is_common",
        ),
        migrations.AddField(
            model_name="channel",
            name="members",
            field=models.ManyToManyField(
                related_name="members", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="channel",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.NablaGroup",
            ),
        ),
    ]

# Generated by Django 3.1.14 on 2022-02-09 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0005_auto_20210927_0206"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ballotcontainer",
            name="alternative",
        ),
        migrations.AddField(
            model_name="ballotcontainer",
            name="current_alternative",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ballots",
                to="vote.alternative",
            ),
        ),
    ]

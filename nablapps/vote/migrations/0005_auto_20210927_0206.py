# Generated by Django 3.1.13 on 2021-09-27 02:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vote", "0004_votingevent_eligible_group"),
    ]

    operations = [
        migrations.CreateModel(
            name="BallotContainer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "alternative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ballots",
                        to="vote.alternative",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="voting",
            name="num_winners",
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name="BallotEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("priority", models.IntegerField()),
                (
                    "alternative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vote.alternative",
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="vote.ballotcontainer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="ballotcontainer",
            name="voting",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ballots",
                to="vote.voting",
            ),
        ),
    ]

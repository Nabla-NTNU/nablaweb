# Generated by Django 2.1.13 on 2020-01-29 19:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("apply_committee", "0001_initial"),
        ("apply_committee", "0002_auto_20200125_1306"),
        ("apply_committee", "0003_auto_20200129_1850"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
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
                ("application_text", models.TextField(blank=True)),
                (
                    "anonymous",
                    models.BooleanField(
                        help_text="Bruker ønsker å være anonym på søkerlisten"
                    ),
                ),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ApplicationRound",
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
                    "name",
                    models.CharField(
                        help_text="Navn på opptaksrunde, f.eks. vår 2022", max_length=20
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text="Er aktiv nå. Kun en opptaksrunde kan være aktiv om gangen.",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Committee",
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
                ("name", models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name="application",
            name="application_round",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="apply_committee.ApplicationRound",
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="committee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="apply_committee.Committee",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="application",
            unique_together={
                ("application_round", "applicant", "priority"),
                ("application_round", "applicant", "committee"),
            },
        ),
    ]

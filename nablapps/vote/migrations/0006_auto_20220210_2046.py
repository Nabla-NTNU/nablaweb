# Generated by Django 3.1.14 on 2022-02-10 20:46

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name="votingevent",
            name="require_checkin",
            field=models.BooleanField(
                default=True, verbose_name="Users must check in to submit votes"
            ),
        ),
        migrations.AddField(
            model_name="votingevent",
            name="users_should_poll",
            field=models.BooleanField(
                default=False, verbose_name="Clients should poll for updates"
            ),
        ),
        migrations.AlterField(
            model_name="ballotentry",
            name="priority",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="votingevent",
            name="checked_in_users",
            field=models.ManyToManyField(
                blank=True, related_name="checked_in_users", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]

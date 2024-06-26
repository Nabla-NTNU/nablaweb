# Generated by Django 3.0.7 on 2021-02-03 19:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vote", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="votingevent",
            options={"permissions": [("vote_admin", "can administer voting")]},
        ),
        migrations.AlterField(
            model_name="voting",
            name="users_voted",
            field=models.ManyToManyField(
                blank=True, related_name="users_voted", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]

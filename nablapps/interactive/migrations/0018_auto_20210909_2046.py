# Generated by Django 3.1.13 on 2021-09-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0017_quiz_spoiler_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="published",
            field=models.BooleanField(
                default=True, null=True, verbose_name="Publisert"
            ),
        ),
        migrations.AlterField(
            model_name="test",
            name="published",
            field=models.BooleanField(
                default=True, null=True, verbose_name="Publisert"
            ),
        ),
    ]

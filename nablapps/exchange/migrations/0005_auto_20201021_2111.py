# Generated by Django 3.0.7 on 2020-10-21 21:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0004_university_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchange",
            name="annet",
            field=models.TextField(blank=True, help_text="Annet.", null=True),
        ),
        migrations.AddField(
            model_name="exchange",
            name="facebook",
            field=models.CharField(
                blank=True,
                help_text="Link til din facebookprofil (valgfritt).",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="exchange",
            name="fag",
            field=models.TextField(blank=True, help_text="Fag du tok.", null=True),
        ),
    ]

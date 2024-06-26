# Generated by Django 3.0.7 on 2020-12-19 21:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0016_placegrid_uncertainty"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="spoiler_html",
            field=models.TextField(
                default="",
                blank=True,
                help_text="HTML som vises til brukeren etter den har sendt inn et svar på quizen. Vises ikke dersom den står tom.",
                verbose_name="Spoiler HTML",
            ),
        ),
    ]

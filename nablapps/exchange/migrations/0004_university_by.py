# Generated by Django 3.0.7 on 2020-10-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchange", "0003_exchangenewsarticle"),
    ]

    operations = [
        migrations.AddField(
            model_name="university",
            name="by",
            field=models.CharField(
                default="",
                help_text="Byen universitetet ligger i",
                max_length=30,
                verbose_name="by",
            ),
        ),
    ]

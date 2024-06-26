# Generated by Django 2.1.7 on 2019-03-26 00:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0008_auto_20171017_0111"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="ignoreCrop",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="Beskjæringen vil bli ignorert og bildet vises i originalt format, med hvit bakgrunn",
                verbose_name="Vis i full størrelse",
            ),
        ),
    ]

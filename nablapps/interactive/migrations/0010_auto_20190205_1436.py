# Generated by Django 2.1.5 on 2019-02-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0009_auto_20190205_1416"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quiz",
            name="publication_date",
        ),
        migrations.AlterField(
            model_name="quiz",
            name="published",
            field=models.NullBooleanField(default=True, verbose_name="Publisert"),
        ),
    ]

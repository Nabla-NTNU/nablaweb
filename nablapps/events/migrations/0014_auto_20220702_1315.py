# Generated by Django 3.1.14 on 2022-07-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0013_auto_20210909_2046"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventregistration",
            name="penalty",
            field=models.IntegerField(
                blank=True,
                default=None,
                help_text="Antall prikker burkeren har fått",
                null=True,
                verbose_name="Prikk",
            ),
        ),
    ]
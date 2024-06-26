# Generated by Django 3.0.7 on 2020-08-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_auto_20190204_2011"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nablauser",
            name="ntnu_card_number",
            field=models.CharField(
                blank=True,
                help_text="Dette er et 7-10-sifret nummer på baksiden av kortet. På nye kort er dette sifrene etter EM. På gamle kort er dette sifrene nede til venstre. Det kan brukes of å identifisere deg på bedriftspresentasjoner og andre arrangementer. ",
                max_length=10,
                verbose_name="NTNU kortnr",
            ),
        ),
    ]

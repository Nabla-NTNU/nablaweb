# Generated by Django 3.1.14 on 2022-07-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interactive", "0025_auto_20220403_2011"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="result",
            options={"ordering": ("length",)},
        ),
        migrations.AlterField(
            model_name="game",
            name="url",
            field=models.TextField(
                help_text="Denne lenken må være relativ ettersom den settes sammen med url-en vår. Altså: hvis man vil lenke til https://nabla.no/kodegolf/ må man skrive inn 'kodegolf/' (uten fnutter). (Ikke hele lenken, da får man: https://nabla.no/https://nabla.no/kodegolf/, som ikke fungerer.)"
            ),
        ),
    ]
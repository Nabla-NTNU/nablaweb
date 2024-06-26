# Generated by Django 3.1.14 on 2022-07-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nablashop", "0003_auto_20211007_1933"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="pris"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="stock",
            field=models.IntegerField(default=0, verbose_name="antall"),
        ),
    ]

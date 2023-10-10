# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        verbose_name="Kategorisk navn",
                        max_length=30,
                        default="Kategori",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        verbose_name="Beskrivelse", default="Her ligger masse rart"
                    ),
                ),
            ],
            options={
                "verbose_name": "Kategori",
                "verbose_name_plural": "Kategorier",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        auto_created=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        verbose_name="Navn", max_length=255, default="Produkt"
                    ),
                ),
                (
                    "description_short",
                    models.TextField(verbose_name="Kort beskrivelse", default="Ting"),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Beskrivelse", default="Ting"),
                ),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                (
                    "photo",
                    models.ImageField(verbose_name="bilde", upload_to="product_photo"),
                ),
                (
                    "price",
                    models.DecimalField(
                        max_digits=5,
                        verbose_name="pris",
                        default="123",
                        decimal_places=2,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        blank=True,
                        to="nablashop.Category",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "Produkt",
                "verbose_name_plural": "Produkter",
            },
        ),
    ]

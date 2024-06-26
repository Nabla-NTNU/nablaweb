# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-30 19:36
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import mptt.fields

from nablapps.album.models import Album


def rebuild_album_tree(apps, schema_editor):
    Album.objects.rebuild()


class Migration(migrations.Migration):
    dependencies = [
        ("album", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="album",
            name="level",
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="album",
            name="lft",
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="album",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="album.Album",
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="rght",
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="album",
            name="tree_id",
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="albumimage",
            name="num",
            field=models.PositiveIntegerField(
                blank=True, editable=False, null=True, verbose_name="Nummer"
            ),
        ),
        migrations.RunPython(rebuild_album_tree),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_auto_20170920_1310"),
    ]

    operations = [
        migrations.RemoveField(model_name="company", name="created_by",),
        migrations.RemoveField(model_name="company", name="created_date",),
        migrations.RemoveField(model_name="company", name="last_changed_by",),
        migrations.RemoveField(model_name="company", name="last_changed_date",),
        migrations.RemoveField(model_name="company", name="publication_date",),
        migrations.RemoveField(model_name="company", name="published",),
        migrations.RemoveField(model_name="company", name="view_counter",),
        migrations.AlterField(
            model_name="company",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]

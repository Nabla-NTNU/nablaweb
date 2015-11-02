# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_auto_20151102_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('file', models.FileField(verbose_name='Bildefil', upload_to='')),
                ('description', models.TextField(verbose_name='Bildetekst', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Innholdsbilde',
            },
        ),
    ]

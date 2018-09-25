# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralOptions',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('favicon', models.ImageField(upload_to='', blank=True)),
                ('site', models.OneToOneField(to='sites.Site', on_delete=models.CASCADE)),
            ],
        ),
    ]

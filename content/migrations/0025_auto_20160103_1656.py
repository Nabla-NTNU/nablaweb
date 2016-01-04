# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0024_auto_20160103_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumimage',
            name='file',
            field=models.ImageField(upload_to='uploads/content', verbose_name='Bildefil'),
        ),
        migrations.AlterField(
            model_name='contentimage',
            name='file',
            field=models.ImageField(upload_to='uploads/content', verbose_name='Bildefil'),
        ),
    ]

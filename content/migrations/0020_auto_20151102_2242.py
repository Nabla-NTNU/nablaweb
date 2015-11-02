# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_auto_20151102_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumimage',
            name='file',
            field=models.FileField(upload_to='uploads/content', verbose_name='Bildefil'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='blog',
            field=models.ForeignKey(related_name='posts', to='content.Blog', verbose_name='Blogg'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(help_text='Her kan du skrive i Markdown', verbose_name='Innhold'),
        ),
        migrations.AlterField(
            model_name='contentimage',
            name='file',
            field=models.FileField(upload_to='uploads/content', verbose_name='Bildefil'),
        ),
        migrations.AlterField(
            model_name='news',
            name='published',
            field=models.NullBooleanField(help_text='Dato har høyere prioritet enn dette feltet.', verbose_name='Publisert', default=True),
        ),
    ]

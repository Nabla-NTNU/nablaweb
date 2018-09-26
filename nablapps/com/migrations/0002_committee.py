# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('com', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('group', models.OneToOneField(primary_key=True, serialize=False, to='auth.Group', verbose_name='Gruppe', on_delete=models.CASCADE)),
                ('mail_list', models.EmailField(blank=True, max_length=254, verbose_name='Epostliste')),
                ('name', models.CharField(unique=True, max_length=80, verbose_name='name')),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Leder', on_delete=models.CASCADE)),
                ('page', models.OneToOneField(to='com.ComPage', blank=True, verbose_name='Komitéside', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Komité',
                'verbose_name_plural': 'Komitéer',
            },
        ),
    ]

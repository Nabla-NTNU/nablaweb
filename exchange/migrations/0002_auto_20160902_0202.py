# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exchange',
            options={'verbose_name': ('utveksling',), 'verbose_name_plural': 'utvekslinger', 'ordering': ['student']},
        ),
        migrations.AlterModelOptions(
            name='info',
            options={'verbose_name': ('info',), 'verbose_name_plural': 'info'},
        ),
        migrations.AlterModelOptions(
            name='university',
            options={'verbose_name': 'universitet', 'verbose_name_plural': 'universiteter', 'ordering': ['univ_navn']},
        ),
        migrations.AddField(
            model_name='university',
            name='desc',
            field=models.TextField(verbose_name='beskrivelse', help_text='En kort beskrivelse av universitetet. Valgfritt.', blank=True),
        ),
    ]

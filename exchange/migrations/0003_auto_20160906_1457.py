# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_auto_20160902_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='retning',
            field=models.CharField(choices=[('biofys', 'Biofysikk og medisinteknologi'), ('indmat', 'Industriell matematikk'), ('tekfys', 'Teknisk fysikk')], help_text='Retning', max_length=6),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20160828_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='retning',
            field=models.CharField(choices=[('Biofysikk og medisinteknologi', 'biofys'), ('Industriell matematikk', 'indmat'), ('Teknisk fysikk', 'tekfys')], help_text='Retning', max_length=30),
        ),
    ]

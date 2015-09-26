# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bedpres', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedpres',
            name='bpcid',
            field=models.CharField(verbose_name='BPC-id', max_length=16, help_text="Dette er id'en som blir brukt internt hos BPC. Ikke endre den hvis du ikke vet hva du gjør.", unique=True),
        ),
    ]

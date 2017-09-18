# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150925_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationrequest',
            name='first_name',
            field=models.CharField(max_length=80, null=True, verbose_name='Fornavn'),
        ),
        migrations.AddField(
            model_name='registrationrequest',
            name='last_name',
            field=models.CharField(max_length=80, null=True, verbose_name='Etternavn'),
        ),
    ]

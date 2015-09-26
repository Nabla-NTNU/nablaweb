# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_registrationrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationrequest',
            options={'verbose_name': 'Registreringsforespørsel', 'verbose_name_plural': 'Registreringsforespørsler'},
        ),
    ]

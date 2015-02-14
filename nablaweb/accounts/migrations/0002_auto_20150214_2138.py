# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150214_2044'),
        ('com', '0001_initial'),
        ('bedpres', '0003_auto_20141013_1716'),
        ('accounts', '0001_initial'),
    ]

    operations = [
#        migrations.RemoveField(
#            model_name='groupleader',
#            name='leads',
#        ),
        migrations.DeleteModel(
            name='GroupLeader',
        ),
    ]

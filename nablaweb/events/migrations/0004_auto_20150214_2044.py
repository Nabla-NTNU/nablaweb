# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_remove_eventpenalty'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together=set([('number', 'attending'), ('event', 'user')]),
        ),
    ]

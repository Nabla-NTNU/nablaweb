# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('jobs', '0001_initial'),
        ('bedpres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedpres',
            name='company',
            field=models.ForeignKey(verbose_name=b'Bedrift', to='jobs.Company', help_text=b'Hvilken bedrift som st\xc3\xa5r bak bedriftspresentasjonen'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bedpres',
            name='open_for',
            field=models.ManyToManyField(help_text=b'Hvilke grupper som f\xc3\xa5r lov til \xc3\xa5 melde seg p\xc3\xa5 arrangementet. Hvis ingen grupper er valgt er det \xc3\xa5pent for alle.', to='auth.Group', null=True, verbose_name=b'\xc3\x85pen for', blank=True),
            preserve_default=True,
        ),
    ]

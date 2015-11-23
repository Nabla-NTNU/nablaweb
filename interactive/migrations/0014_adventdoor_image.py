# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive', '0013_adventdoor_is_text_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventdoor',
            name='image',
            field=models.ImageField(upload_to='', null=True, blank=True, verbose_name='Bilde'),
        ),
    ]

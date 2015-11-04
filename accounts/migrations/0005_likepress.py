# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150927_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('reference_id', models.IntegerField(null=True)),
                ('model_name', models.CharField(null=True, max_length=100)),
                ('user', models.ForeignKey(related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

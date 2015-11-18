# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interactive', '0011_quiz_content_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdventParticipation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('when', models.DateTimeField(auto_created=True)),
                ('text', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='adventdoor',
            name='participating_users',
        ),
        migrations.RemoveField(
            model_name='adventdoor',
            name='users',
        ),
        migrations.AddField(
            model_name='adventparticipation',
            name='door',
            field=models.ForeignKey(related_name='participation', to='interactive.AdventDoor'),
        ),
        migrations.AddField(
            model_name='adventparticipation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

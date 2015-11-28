# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0022_auto_20151106_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplashConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('cookie_name', models.TextField(help_text='The name of the cookie to check when assessing if the user needs to be redirected', default='splash_screen')),
                ('cookie_allowed_values', models.TextField(help_text='Comma-separated list of values accepted as cookie values to prevent the redirect', default='seen')),
                ('unaffected_usernames', models.TextField(help_text='Comma-separated list of users which should never be redirected (usernames)', blank=True, default='')),
                ('unaffected_url_paths', models.TextField(help_text='Comma-separated list of URL paths (not including the hostname) which should not be redirected. Paths may include wildcards denoted by * (example: /*/student_view)', blank=True, default='')),
                ('redirect_url', models.URLField(help_text="The URL the users should be redirected to when they don't have the right cookie", default='https://nabla.no')),
                ('changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='Changed by')),
            ],
            options={
                'abstract': False,
                'ordering': ('-change_date',),
            },
        ),
    ]

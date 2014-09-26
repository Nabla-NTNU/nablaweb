# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NablaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telephone', models.CharField(max_length=15, verbose_name=b'Telefon', blank=True)),
                ('cell_phone', models.CharField(max_length=15, verbose_name=b'Mobil', blank=True)),
                ('birthday', models.DateField(null=True, verbose_name=b'Bursdag', blank=True)),
                ('address', models.CharField(max_length=40, verbose_name=b'Adresse', blank=True)),
                ('mail_number', models.CharField(max_length=4, verbose_name=b'Postnr', blank=True)),
                ('web_page', models.CharField(max_length=80, verbose_name=b'Hjemmeside', blank=True)),
                ('wants_email', models.BooleanField(default=True, verbose_name=b'Motta kullmail')),
                ('about', models.TextField(verbose_name=b'Biografi', blank=True)),
                ('avatar', models.ImageField(upload_to=b'avatars', null=True, verbose_name=b'Avatar', blank=True)),
                ('ntnu_card_number', models.CharField(help_text=b'Dette er det 7-10 siffer lange nummeret <b>nede til venstre</b> p\xc3\xa5 baksiden av NTNU-adgangskortet ditt. Det brukes blant annet for \xc3\xa5 komme inn p\xc3\xa5 bedpresser.', max_length=10, verbose_name=b'NTNU kortnr', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NablaGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('description', models.TextField(verbose_name=b'Beskrivelse', blank=True)),
                ('mail_list', models.EmailField(max_length=75, verbose_name=b'Epostliste', blank=True)),
                ('group_type', models.CharField(blank=True, max_length=10, choices=[(b'komite', b'Komit\xc3\xa9'), (b'kull', b'Kull'), (b'studprog', b'Studieprogram'), (b'komleder', b'Komit\xc3\xa9leder'), (b'styremedlm', b'Styremedlem'), (b'stilling', b'Stilling')])),
            ],
            options={
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='GroupLeader',
            fields=[
                ('leads', models.OneToOneField(related_name=b'leader', primary_key=True, serialize=False, to='accounts.NablaGroup')),
            ],
            options={
            },
            bases=('accounts.nablagroup',),
        ),
        migrations.CreateModel(
            name='FysmatClass',
            fields=[
                ('nablagroup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='accounts.NablaGroup')),
                ('starting_year', models.CharField(unique=True, max_length=4, verbose_name=b'\xc3\x85r startet')),
            ],
            options={
                'verbose_name': 'Kull',
                'verbose_name_plural': 'Kull',
            },
            bases=('accounts.nablagroup',),
        ),
        migrations.AddField(
            model_name='nablauser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nablauser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]

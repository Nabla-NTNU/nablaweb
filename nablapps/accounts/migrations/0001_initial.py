# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='NablaUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=30, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('telephone', models.CharField(blank=True, max_length=15, verbose_name='Telefon')),
                ('cell_phone', models.CharField(blank=True, max_length=15, verbose_name='Mobil')),
                ('birthday', models.DateField(null=True, blank=True, verbose_name='Bursdag')),
                ('address', models.CharField(blank=True, max_length=40, verbose_name='Adresse')),
                ('mail_number', models.CharField(blank=True, max_length=4, verbose_name='Postnr')),
                ('web_page', models.CharField(blank=True, max_length=80, verbose_name='Hjemmeside')),
                ('wants_email', models.BooleanField(verbose_name='Motta kullmail', default=True)),
                ('about', models.TextField(blank=True, verbose_name='Biografi')),
                ('avatar', models.ImageField(null=True, blank=True, upload_to='avatars', verbose_name='Avatar')),
                ('ntnu_card_number', models.CharField(help_text="Dette er et 7-10 siffer lant nummeret på baksiden av kortet. På nye kort er dette siffrene etter EM. På gamle kort ert dette siffrene nede til venstre. Det brukes blant annet for å komme inn på bedpresser." , blank=True, max_length=10, verbose_name='NTNU kortnr')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='NablaGroup',
            fields=[
                ('group_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='auth.Group', on_delete=models.CASCADE)),
                ('description', models.TextField(blank=True, verbose_name='Beskrivelse')),
                ('mail_list', models.EmailField(blank=True, max_length=254, verbose_name='Epostliste')),
                ('group_type', models.CharField(blank=True, max_length=10, choices=[('komite', 'Komité'), ('kull', 'Kull'), ('studprog', 'Studieprogram'), ('komleder', 'Komitéleder'), ('styremedlm', 'Styremedlem'), ('stilling', 'Stilling')])),
            ],
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='FysmatClass',
            fields=[
                ('nablagroup_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='accounts.NablaGroup', on_delete=models.CASCADE)),
                ('starting_year', models.CharField(unique=True, max_length=4, verbose_name='År startet')),
            ],
            options={
                'verbose_name_plural': 'Kull',
                'verbose_name': 'Kull',
            },
            bases=('accounts.nablagroup',),
        ),
        migrations.AddField(
            model_name='nablauser',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_name='user_set', related_query_name='user', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='nablauser',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', blank=True, related_name='user_set', related_query_name='user', verbose_name='user permissions'),
        ),
    ]

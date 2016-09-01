# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('retning', models.CharField(max_length=30, choices=[('biofys', 'Biofysikk og medisinteknologi'), ('indmat', 'Industriell matematikk'), ('tekfys', 'Teknisk fysikk')], help_text='Retning')),
                ('start', models.DateField(help_text='Dato utveksling startet')),
                ('end', models.DateField(help_text='Dato utveksling sluttet')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['student'],
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='flatpages.FlatPage', primary_key=True)),
                ('ex', models.ForeignKey(to='exchange.Exchange')),
            ],
            bases=('flatpages.flatpage',),
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('univ_navn', models.CharField(verbose_name='universitets navn', max_length=50, default='', help_text='Navnet til universitetet')),
                ('land', models.TextField(verbose_name='land', max_length=30, default='', help_text='Landet universitetet ligger i')),
            ],
            options={
                'ordering': ['univ_navn'],
            },
        ),
        migrations.DeleteModel(
            name='Link',
        ),
        migrations.DeleteModel(
            name='Universitet',
        ),
        migrations.DeleteModel(
            name='Utveksling',
        ),
        migrations.AddField(
            model_name='exchange',
            name='univ',
            field=models.ForeignKey(to='exchange.University'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0004_auto_20150525_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Sesongnummer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='podcast',
            options={'verbose_name_plural': 'Podcast', 'ordering': ['-pub_date'], 'verbose_name': 'Podcast'},
        ),
        migrations.AddField(
            model_name='podcast',
            name='is_clip',
            field=models.BooleanField(verbose_name='Er lydklipp', default=False, help_text='Lydklipp blir ikke vist sammen med episodene.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='podcast',
            name='season',
            field=models.ForeignKey(verbose_name='Sesong', null=True, blank=True, to='podcast.Season'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='podcast',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '300x300', hide_image_field=False, size_warning=False, free_crop=False, verbose_name='Beskjæring', adapt_rotation=False, allow_fullsize=False, help_text='Bildet vises i full form på detaljsiden.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='podcast',
            name='image',
            field=models.ImageField(verbose_name='Bilde', null=True, upload_to='news_pictures', blank=True, help_text='Bilder som er større enn 300x300 px ser best ut. Du kan beskjære bildet etter opplasting.'),
            preserve_default=True,
        ),
    ]

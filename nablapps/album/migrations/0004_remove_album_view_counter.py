# Generated by Django 2.1.5 on 2019-02-05 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("album", "0003_albumimage_is_display_image"),
    ]

    operations = [
        migrations.RemoveField(model_name="album", name="view_counter",),
    ]

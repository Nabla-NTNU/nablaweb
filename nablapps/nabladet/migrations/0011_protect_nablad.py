# Generated by Django 2.1.7 on 2019-03-28 19:59

import os
from shutil import move

import django.core.files.storage
from django.conf import settings
from django.db import migrations, models


def move_to_protected(apps, schema_editor):
    """Move existing nablads from MEDIA_ROOT/nabladet to PROTECTED_MEDIA_ROOT/nabladet
    This is really a one-off, because we move existing nablads to protect"""

    src = os.path.join(settings.MEDIA_ROOT, "nabladet")
    dst = os.path.join(settings.PROTECTED_MEDIA_ROOT, "nabladet")

    if not os.path.exists(src) or os.path.exists(dst):
        # Nothing to to
        return
    move(src, dst)


def undo_move_to_protected(apps, schema_editor):
    src = os.path.join(settings.PROTECTED_MEDIA_ROOT, "nabladet")
    dst = os.path.join(settings.MEDIA_ROOT, "nabladet")
    move(src, dst)


class Migration(migrations.Migration):

    dependencies = [
        ("nabladet", "0010_nablad_file_nsfw"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nablad",
            name="file",
            field=models.FileField(
                help_text="Filnavn. OBS: opplasting kan ta rundt ett minutt, så bare trykk 'Lagre' én gang.",
                storage=django.core.files.storage.FileSystemStorage(
                    location=settings.PROTECTED_MEDIA_ROOT
                ),
                upload_to="nabladet",
                verbose_name="PDF-fil",
            ),
        ),
        migrations.AlterField(
            model_name="nablad",
            name="file_nsfw",
            field=models.FileField(
                blank=True,
                help_text="Filnavn",
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location=settings.PROTECTED_MEDIA_ROOT
                ),
                upload_to="nabladet",
                verbose_name="PDF-fil NSFW",
            ),
        ),
        migrations.AlterField(
            model_name="nablad",
            name="thumbnail",
            field=models.FileField(
                editable=False,
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location=settings.PROTECTED_MEDIA_ROOT
                ),
                upload_to="",
            ),
        ),
        migrations.RunPython(move_to_protected, undo_move_to_protected),
    ]

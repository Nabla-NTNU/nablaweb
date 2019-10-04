"""Moves objects from bedpres to events

Note that bedpres has to be an installed app for this migration
to do anything. So if you wish to copy objects from bedpres to
evnets in order to be able to delete bedpres, you must apply
this migration before removing bedpres from apps"""

from django.apps import apps as global_apps
from django.db import migrations

# Fields that need no special treatment
fields_to_copy = [
    "picture",
    "cropping",
    "headline",
    "slug",
    "short_name",
    "lead_paragraph",
    "company",
    "organizer",
    "location",
    "event_start",
    "event_end",
    "registration_required",
    "registration_deadline",
    "registration_start",
    "deregistration_deadline",
    "places",
    "has_queue",
    "facebook_url"]

def forwards_func(apps, schema_editor):
    try:
        BedPres = apps.get_model("bedpres", "BedPres")
    except LookupError:
        # BedPres not installed, nothing to do
        print("bedpres not installed, nothing to do")
        return

    Event = apps.get_model("events", "Event")

    for bed in BedPres.objects.all():
        event = Event(is_bedpres=True, company=bed.company)

        for field in fields_to_copy:
            setattr(event, field, getattr(bed, field))
        # Want to save BPC id
        body = bed.body + "\nPBC id: " + bed.bpcid
        event.body = body
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_add_fields_from_bedpres_and_penalty'),
    ]

    if global_apps.is_installed('bedpres'):
        dependencies.append(('bedpres', '0002_auto_20190205_1251.py'))

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]

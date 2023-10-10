# open_for in RegistrationInfoMixins in mixins to events can only be applied to FysmatClass objects

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0004_move_bedpres_objects_to_event_20191003"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="open_for",
            field=models.ManyToManyField(
                blank=True,
                help_text="Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.",
                to="accounts.FysmatClass",
                verbose_name="Åpen for",
            ),
        ),
    ]

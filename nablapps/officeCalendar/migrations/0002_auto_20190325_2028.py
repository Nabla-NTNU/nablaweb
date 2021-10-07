import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("officeCalendar", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="officeevent",
            name="duration",
        ),
        migrations.AddField(
            model_name="officeevent",
            name="end_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="officeevent",
            name="public",
            field=models.BooleanField(
                default=False, help_text="Synlig for alle, uten å logge inn"
            ),
        ),
        migrations.AddField(
            model_name="officeevent",
            name="repeating",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="officeevent",
            name="start_time",
            field=models.DateTimeField(
                help_text="Reservasjoner mellom 11:00 og 13:00 krever styrets godkjenning."
            ),
        ),
    ]

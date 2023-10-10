# Changed field type for transaction description from CharField to TextField.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("officeBeer", "0002_depositrequest_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="description",
            field=models.TextField(verbose_name="Forklaring av transaksjon"),
        ),
    ]

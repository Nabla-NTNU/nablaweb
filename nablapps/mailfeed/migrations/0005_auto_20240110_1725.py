# Generated by Django 3.2.23 on 2024-01-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailfeed", "0004_subscription_email_hash"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="email_hash",
        ),
        migrations.AddField(
            model_name="subscription",
            name="uuid",
            field=models.CharField(default=23, max_length=150),
            preserve_default=False,
        ),
    ]

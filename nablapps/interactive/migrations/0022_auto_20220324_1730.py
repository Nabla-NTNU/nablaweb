# Generated by Django 3.1.14 on 2022-03-24 17:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0021_codegolf_result_unique"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="result",
            name="code_golf_result_unique_task_user",
        ),
    ]

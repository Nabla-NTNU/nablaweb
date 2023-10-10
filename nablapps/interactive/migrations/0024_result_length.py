from django.db import migrations, models

from nablapps.interactive.models.code_golf import Result


def empty_reverse(*args):
    """Some empty callable to fake reverse"""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("interactive", "0023_result_python_version"),
    ]

    def set_length(apps, schema_editor):
        for result in Result.objects.all():
            result.length = len(result.solution.strip())
            result.save()

    operations = [
        migrations.AddField(
            model_name="result",
            name="length",
            field=models.IntegerField(null=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_length, empty_reverse),
        migrations.AlterField(
            model_name="result",
            name="length",
            field=models.IntegerField(null=False),
        ),
    ]

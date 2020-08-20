# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_like_presses(apps, schema_editor):
    OldLikePress = apps.get_model("accounts", "LikePress")
    NewLikePress = apps.get_model("likes", "LikePress")
    ContentType = apps.get_model("contenttypes", "ContentType")
    for old in OldLikePress.objects.all():
        new = NewLikePress()
        content_types = ContentType.objects.order_by("-id").filter(model=old.model_name)
        new.content_type = content_types.first()
        new.object_id = old.reference_id
        new.user = old.user
        new.save()


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("accounts", "0006_auto_20160202_2330"),
    ]

    operations = [
        migrations.RunPython(copy_like_presses),
        migrations.RemoveField(model_name="likepress", name="user",),
        migrations.DeleteModel(name="LikePress",),
    ]

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "created",
                    models.DateField(verbose_name="Opprettet", auto_now_add=True),
                ),
                ("name", models.CharField(max_length=80, verbose_name="Navn")),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                "verbose_name": "Blogg",
                "verbose_name_plural": "Blogger",
                "db_table": "content_blog",
            },
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Publiseringsdato", null=True
                    ),
                ),
                (
                    "last_changed_date",
                    models.DateTimeField(
                        verbose_name="Redigeringsdato", null=True, auto_now=True
                    ),
                ),
                ("title", models.CharField(max_length=80, verbose_name="Tittel")),
                (
                    "content",
                    models.TextField(
                        help_text="Her kan du skrive i Markdown", verbose_name="Innhold"
                    ),
                ),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "allow_comments",
                    models.BooleanField(
                        help_text="Hvorvidt kommentering er tillatt",
                        verbose_name="Tillat kommentarer",
                        default=True,
                    ),
                ),
                (
                    "blog",
                    models.ForeignKey(
                        related_name="posts",
                        to="blog.Blog",
                        verbose_name="Blogg",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="blogpost_created",
                        editable=False,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Opprettet av",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "last_changed_by",
                    models.ForeignKey(
                        related_name="blogpost_edited",
                        editable=False,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Endret av",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "view_counter",
                    models.IntegerField(
                        editable=False, verbose_name="Visninger", default=0
                    ),
                ),
                (
                    "list_image",
                    models.ImageField(
                        upload_to="blogpics",
                        blank=True,
                        help_text="Bilde som vises i listevisningen av bloggene",
                        verbose_name="Listebilde",
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Poster",
                "db_table": "content_blogpost",
            },
        ),
    ]

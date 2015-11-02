
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from datetime import date

from .base import EditableMedia


class Blog(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name="Navn"
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        editable=True,
    )

    created = models.DateField(
        editable=False,
        verbose_name="Opprettet"
    )

    class Meta:
        verbose_name = "Blogg"
        verbose_name_plural = "Blogger"

    def save(self, **kwargs):
        if not self.id:
            self.created = date.today()
        self.slug = slugify(self.name)
        return super().save(**kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog', kwargs={'blog': self.slug})


class BlogPost(EditableMedia, models.Model):
    blog = models.ForeignKey(
        "content.Blog",
        related_name="posts",
        verbose_name="Blogg"
    )

    title = models.CharField(
        max_length=80,
        verbose_name="Tittel"
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=True,
    )

    content = models.TextField(
        verbose_name="Innhold",
        help_text="Her kan du skrive i Markdown"
    )

    allow_comments = models.BooleanField(
        blank=True,
        verbose_name="Tillat kommentarer",
        default=True,
        help_text="Hvorvidt kommentering er tillatt"
    )

    watch_fields = ["content", "title", "blog"]

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Poster"

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        return super().save(**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post', kwargs={'blog': self.blog.slug, 'slug': self.slug})

# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from image_cropping.fields import ImageRatioField, ImageCropField
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment

class PolymorphicMetaclass(ModelBase):
    """
    https://code.google.com/p/django-polymorphic-models/

    Legger til content_type og downcast()-metoder.
    """
    def __new__(cls, name, bases, dct):
        def save(self, *args, **kwargs):
            if(not self.content_type):
                self.content_type = ContentType.objects.get_for_model(self.__class__)
            models.Model.save(self, *args, **kwargs)

        def downcast(self):
            model = self.content_type.model_class()
            if (model == self.__class__):
                return self
            return model.objects.get(id=self.id)

        if issubclass(dct.get('__metaclass__', type), PolymorphicMetaclass):
            dct['content_type'] = models.ForeignKey(ContentType, editable=False, null=True)
            dct['save'] = save
            dct['downcast'] = downcast

        return super(PolymorphicMetaclass, cls).__new__(cls, name, bases, dct)


class DowncastMetaclass(PolymorphicMetaclass):
    def __new__(cls, name, bases, dct):
        dct['objects'] = DowncastManager()
        return super(DowncastMetaclass, cls).__new__(cls, name, bases, dct)


class DowncastManager(models.Manager):
    def get_query_set(self):
        return DowncastQuerySet(self.model)


class DowncastQuerySet(QuerySet):

    def __getitem__(self, k):
        result = super(DowncastQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.downcast()
        else:
            return result

    def __iter__(self):
        for item in super(DowncastQuerySet, self).__iter__():
            yield item.downcast()


class Content(models.Model):

    __metaclass__ = PolymorphicMetaclass

    # Metadata
    created_date = models.DateTimeField(verbose_name="Publiseringsdato", auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name="Opprettet av", related_name="%(class)s_created", editable=False, blank=True, null=True)
    last_changed_date = models.DateTimeField(verbose_name="Redigeringsdato", auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, verbose_name="Endret av", related_name="%(class)s_edited", editable=False, blank=True, null=True)

    # Bildeopplasting med resizing og cropping
    picture = ImageCropField(upload_to="news_pictures", null=True, blank=True, verbose_name="Bilde", help_text="Bilder som er større enn 770x300 px ser best ut. Du kan beskjære bildet etter opplasting.")
    cropping = ImageRatioField('picture', '770x300', allow_fullsize=False, verbose_name="Beskjæring")

    # Slugs
    slug = models.SlugField(null=True, blank=True, help_text="Denne teksten vises i adressen til siden, og trengs vanligvis ikke å endres")
    
    allow_comments = models.BooleanField(blank=True, verbose_name="Tillat kommentarer", help_text="Hvorvidt kommentering er tillatt", default=True)

    class Meta:
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        """
        Finner URL ved å reversere navnet på viewen.
        Krever at navnet på viewet er gitt ved modellnavn_detail
        """
        return (self.content_type.model + "_detail", (), {
            'pk': self.pk,
            'slug': self.slug
        })

    def has_been_edited(self):
        return abs((self.last_changed_date - self.created_date).seconds) > 1

    def get_picture_url(self):
        return 'http://%s%s%s' % (Site.objects.get_current().domain, settings.MEDIA_URL, self.picture().name)

    def delete(self):
        """
        Override default method, so related comments are also deleted
        """
        comments = Comment.objects.filter(object_pk=self.pk, content_type=self.content_type)
        comments.delete()
        super(Content, self).delete()


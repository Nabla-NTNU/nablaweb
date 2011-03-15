import os, PIL
from django.db import models
from django.dispatch import dispatcher

class Album(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.title

class Picture(models.Model):
    title = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    album = models.ForeignKey(Album)
    picture = models.ImageField(upload_to='temp', blank=True)
    thumbnail = models.ImageField(upload_to='temp', blank=True)
    def __unicode__(self):
        return self.title

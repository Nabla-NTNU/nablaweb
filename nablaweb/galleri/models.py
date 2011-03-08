from django.db import models

# Mye som mangler her fortsatt

class Album(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=true)
    def __unicode__(self):
        return self.title

class Picture(models.Model):
    title = models.CharField(max_length=64, blank=true) #Går ut i fra at det kan være litt slitsomt å navngi alle bilder
    description = models.TextField(blank=true)
    album = models.ForeignKey(Album)
    picture = models.ImageField(upload_to='images') #Ikke ferdig, her må det selvsagt brukes et mer omfattende opplastingsskript
    def __unicode__(self):
        return self.title

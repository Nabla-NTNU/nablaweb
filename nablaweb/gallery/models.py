from django.db import models
from django.dispatch import dispatcher
from django.conf import settings
from PIL import Image

import os
import hashlib
import StringIO

GALLERY_FOLDER = 'gallery'
TEMP_FOLDER = 'temp'

# MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)
GALLERY_DIR = os.path.join(getattr(settings, 'MEDIA_ROOT', None),GALLERY_FOLDER)
TEMP_DIR = os.path.join(getattr(settings, 'MEDIA_ROOT', None),TEMP_FOLDER)

""" Innstillinger for opplastede bilders opplosning """

PICTURE_DIM = 720
PICTURE_DIM_THUMB = 180

""" Globale funksjoner """

# En funksjon som returnerer skalerte verdier paa width og height
def scale_dimensions(width, height, lowest_side):
    if width > height:
        return ( lowest_side, int(height * lowest_side/float(width)) )
    else:
        return ( int(width * lowest_side/float(height)), lowest_side )

""" Selve modellen """

class Album(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.title

class Picture(models.Model):
    title = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    album = models.ForeignKey(Album)
    picture = models.ImageField(upload_to=TEMP_FOLDER, blank=True)
    thumbnail = models.ImageField(upload_to=TEMP_FOLDER, blank=True)
    def __unicode__(self):
        return self.title


    def save(self):
        super(Picture, self).save()
        temp_path = self.picture.path

        # De to tilfellene der noe maa gjores:
        if ( (temp_path.find(GALLERY_DIR) == -1) or not self.thumbnail):
            img = Image.open(temp_path)
            
            # Endrer storrelse paa bilder
            (width, height) = img.size
            resizedImage = img.resize(scale_dimensions(width, height, lowest_side = PICTURE_DIM))
            thumbnail = img.resize(scale_dimensions(width, height, lowest_side = PICTURE_DIM_THUMB))       
            
            # Ordner filnavn og lagringssted
            imagefile = StringIO.StringIO()
            resizedImage.save(imagefile, 'JPEG')
            filename = hashlib.md5(imagefile.getvalue()).hexdigest()
            filename_thumb = filename + '-thumb.jpg'
            filename = filename + '.jpg'
            save_path = os.path.join(GALLERY_DIR,str(self.album.title))
            
            # Oppretter mapper om de ikke finnes
            try:
                os.stat(save_path)
            except:
                os.makedirs(save_path)
            
            # Lagrer thumbnail
            imagefile = open(os.path.join(save_path, filename), 'w')
            resizedImage.save(imagefile, 'JPEG')
            imagefile.close()
            
            # Lagrer thumbnail
            imagefile = open(os.path.join(save_path, filename_thumb), 'w')
            thumbnail.save(imagefile, 'JPEG')
            imagefile.close()
                
            # Django bruker automatisk 'MEDIA_ROOT' som root for ImageFields 
            # saa man kan ikke bruke 'save_path'
            media_path = 'gallery/' + str(self.album.title) + '/'
            self.picture = media_path + filename
            self.thumbnail = media_path + filename_thumb
            
            # Sletter det gamle bildet
            temp_path = img.filename
            os.remove(temp_path)
    
            super(Picture, self).save()


from django.db import models
from django.dispatch import dispatcher
from django.conf import settings
from PIL import Image

import os
import hashlib
import StringIO

GALLERY_DIR = os.path.join(getattr(settings, 'MEDIA_ROOT', None),'gallery')

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
    picture = models.ImageField(upload_to='temp', blank=True)
    thumbnail = models.ImageField(upload_to='temp', blank=True)
    def __unicode__(self):
        return self.title

# HAX
    def manage_uploaded_image(self,posted_picture):
        imagefile = StringIO.StringIO(posted_picture.read())
        img = Image.open(imagefile)
        img.load()
        # For aa oppdage korrupte png-filer (funker ikke atm)
        #img = Image.open(imagefile)
        #img.verify()

        # Endrer storrelse
        (width, height) = img.size
        resizedImage = img.resize(scale_dimensions(width, height, lowest_side = PICTURE_DIM))
        thumbnail = img.resize(scale_dimensions(width, height, lowest_side = PICTURE_DIM_THUMB))

        imagefile = StringIO.StringIO()
        resizedImage.save(imagefile, 'JPEG')
        # Setter filnavn som forhaapentligvis er unikt
        # Litt tungvint aa maatte lagre to ganger, saa det
        # kan vaere noe aa fikse paa til senere
        filename = hashlib.md5(imagefile.getvalue()).hexdigest()
        filename_thumb = filename + '-thumb.jpg'
        filename = filename + '.jpg'
    
        save_path = os.path.join(GALLERY_DIR,str(self.album.title))
    
        try:
            os.stat(save_path)
        except:
            os.makedirs(save_path)
    
        imagefile = open(os.path.join(save_path, filename), 'w')
        resizedImage.save(imagefile, 'JPEG')
        imagefile.close()
    
        imagefile = open(os.path.join(save_path, filename_thumb), 'w')
        thumbnail.save(imagefile, 'JPEG')
        imagefile.close()
            
        # Django bruker automatisk MEDIA_ROOT som root for ImageFields saa man kan ikke bruke 'save_path'
        media_path = 'gallery/' + str(self.album.title) + '/'
        self.picture = media_path + filename
        self.thumbnail = media_path + filename_thumb
        self.save()
    

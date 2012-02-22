# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image

import os
import StringIO
import datetime

#TODO:
# Album-i-album
# Brukertillatelser
# Rotasjon av bilder (funksjoner i Picture?)
# Generell exception handeling i alle try-except-instanser.

GALLERY_FOLDER = 'gallery'
TEMP_FOLDER = 'temp'

GALLERY_DIR = os.path.join(getattr(settings, 'MEDIA_ROOT', None),GALLERY_FOLDER)
TEMP_DIR = os.path.join(getattr(settings, 'MEDIA_ROOT', None),TEMP_FOLDER)

""" Innstillinger for opplastede bilders oppløsning """

PICTURE_DIM = 620
PICTURE_DIM_THUMB = 140

""" Globale funksjoner """

# En funksjon som returnerer skalerte verdier på width og height
def scale_dimensions(width, height, lowest_side):
    if width > height:
        return ( lowest_side, int(height * lowest_side/float(width)) )
    else:
        return ( int(width * lowest_side/float(height)), lowest_side )

""" Selve modellen """

#TODO: Problemer med når album endrer navn av og til
#       må testes. (Bilder som ikke flytter seg ordentlig)
#       test med æøå, spesialtegn og whitespace
class Album(models.Model):
    title = models.CharField('tittel',max_length=64, unique=True, blank = False)
    description = models.TextField('beskrivelse',blank=True)
    pic_increment = models.IntegerField(editable=False, default=-1)
    folder_path = models.CharField(max_length=128,editable=False, blank=True)
    date_published = models.DateTimeField('dato opprettet',auto_now_add=True)
    date_last_changed = models.DateTimeField('sist endret',auto_now=True)
    def __unicode__(self):
        return self.title

    # Øker pic_increment med én og returnerer et navn bildet kan lagres med (Brukes av Picture)
    def getNewPictureName(self): 
        self.pic_increment = self.pic_increment + 1
        super(Album,self).save()
        return self.pic_increment
    
    def update_last_date_changed(self):
        self.date_last_changed = datetime.datetime.now()
        super(Album,self).save()

    def save(self):
        # Sørger for at det finnes en mappe med albumets navn i gallery-mappen
        # Bilder som tilhører albumet vil legges der
        # Dersom navnet til albumet er endret, vil den endre navnet på denne mappen
        # og si i fra til alle bilder at dette har skjedd ved å kalle Picture.album_has_been_renamed()
        # for hvert av bildene.
        self.update_last_date_changed()
        # Fjerner '/' som vil gjøre at det blir lagd mer enn én mappe
        folder_path = os.path.join(GALLERY_DIR,self.title.replace('/',''))
        album_renamed = False
        try:
            os.stat(self.folder_path)
        except:
            try:
                os.stat(folder_path)
            except:
#TODO: Hva hvis mappen finnes fra før?
                os.makedirs(folder_path)
        else:
            if self.folder_path != folder_path:
                try:
                    os.rename(self.folder_path, folder_path)
                except:
                   pass
                else:
                    album_renamed = True
        self.folder_path = folder_path
        super(Album,self).save()
        if album_renamed:
            for pic in self.picture_set.all():
                pic.album_has_been_renamed()

    def delete(self):
        for pic in self.picture_set.all():
            pic.delete()
        try:
            os.stat(self.folder_path)
        except:
            pass
        else:
            try:
                os.rmdir(self.folder_path)
            except:
                pass
        super(Album,self).delete()

class Picture(models.Model):
    
    # Beskrivelse av bildet, dette feltet er frivillig
    description = models.TextField('beskrivelse', blank=True)
    
    # En en-til-mange-relasjon mellom albummet og bildet.
    # Dette må være fylt ut.
    album = models.ForeignKey(Album)
    
    # En variabel som korresponderer med filnavnet til bildefilene.
    # (Dersom variabelen er 10, så vil bildene hete 10.jpg og 10-thumb.jpg)
    # Den blir bestemt av albummets pic_increment, og det trenger ikke
    # nødvendigvis å være noen sammenheng mellom album_picnr og 
    # antall bilder i albummet. (Bilder kan ha blitt slettet)
    album_picnr = models.IntegerField('Plass i albummet', editable=False ,default=-1)
    
    # Her lagres informasjon om bildet (hvor det er lagret).
    # Når man laster opp et bilde vil den først bli lagret i
    # TEMP_FOLDER, for så å bli flyttet når bildet lagres.
    picture = models.ImageField('bilde', upload_to=TEMP_FOLDER)
    
    # Det samme som over. Denne er ment å være tom når man oppretter
    # et Picture-element.
    thumbnail = models.ImageField(upload_to=TEMP_FOLDER, editable=False,  blank=True)
    
    # Inneholder tiden bildet ble lastet opp
    date_published = models.DateTimeField('dato opprettet', auto_now_add=True)
    
    last_changed_date = models.DateTimeField('sist endret', auto_now=True)
    
    # Antall requests bildet har fått. Har i utgangspunktet ikke tenkt å 
    # la den være avhengig av IP eller user.
    number_of_hits = models.IntegerField('antall treff', editable=False, default=0)

    # Eier av bildet (den som lastet det opp)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return u'Picture %s in %s' % (unicode(self.album_picnr),unicode(self.album))

    # Endrer self.picture slik at filnavnene blir riktige etter at mappen
    # til albummet skifter navn. Denne funksjonen kalles bare av Album
    def album_has_been_renamed(self):
        if self.picture:
            self.picture = u'%s%s/%s' % (GALLERY_FOLDER, self.album.folder_path.split(GALLERY_DIR)[-1], str(self.picture).split('/')[-1])
            self.thumbnail = u'%s%s/%s' % (GALLERY_FOLDER, self.album.folder_path.split(GALLERY_DIR)[-1], str(self.thumbnail).split('/')[-1])
            self.save()
        
    # Øker antall treff med 1
    def increment_number_of_hits(self):
        self.number_of_hits += 1
        self.save()
        
    def getPictureUrl(self):
        return u'%s%s' % (getattr(settings, 'MEDIA_URL', None),self.picture)
    
    def getThumbnailUrl(self):
        return u'%s%s' % (getattr(settings, 'MEDIA_URL', None),self.thumbnail)
    
    # Overlagrer slettefunksjonen for å kunne slette bildefilene
    # og oppdatere at albummet har blitt oppdatert/endret
    def delete(self, *args, **kwargs):
        try:
            os.stat(self.picture.path)
        except:
            pass
        else:
            os.remove(self.picture.path)
        try:
            os.stat(self.thumbnail.path)
        except:
            pass
        else:
            os.remove(self.thumbnail.path)
        self.album.update_last_date_changed()
        super(Picture,self).delete(*args, **kwargs)

    # Overlagrer lagringsfunksjonen
    def save(self, *args, **kwargs):
        # Lagrer bildet.
        super(Picture, self).save(*args,**kwargs)
        # Oppdaterer albummet om at det har blitt endret.
        self.album.update_last_date_changed()
        
        # De tilfellene der noe må gjøres:
        if ( (unicode(self.picture.path).find(self.album.folder_path) == -1) or not self.thumbnail):
            # Dersom den oppgitte stien til bildet ikke er et bilde vil ikke
            # resten av koden kjøre
            # Dette skal ideelt aldri skje, da det vil stoppes i form-godkjenningen
            try:
                img = Image.open(self.picture.path)
                print img.filename
            except:
                pass
            else:
                # Endrer størrelse på bilder
                (width, height) = img.size
                resizedImage = img.resize(scale_dimensions(width, height, lowest_side = PICTURE_DIM), Image.ANTIALIAS)
                thumbnail = img.resize(scale_dimensions(width, height, lowest_side = PICTURE_DIM_THUMB), Image.ANTIALIAS)
                
                # Ordner filnavn
                # Dersom bildet har blitt flyttet fra et album til et annet, 
                # må man teste om det finnes et med likt filnavn fra før
                rename_boolean = False
                if self.album_picnr+1:
                    for i in self.album.picture_set.all():
                        if i.album_picnr == self.album_picnr and i.picture != self.picture:
                            rename_boolean = True
                elif self.album_picnr > self.album.pic_increment:
                    rename_boolean = True
                if not self.album_picnr+1 or rename_boolean:
                    self.album_picnr = self.album.getNewPictureName()
    
    
                
                imagefile = StringIO.StringIO()
                #TODO: Redundant?
                resizedImage.save(imagefile, img.format)
                
                # Finner filtype-extension:
                imagetype = unicode(self.picture.path).split('.')[-1]
                
                # Lager filnavn:
                filename_thumb = u'%s-thumb.%s' % (unicode(self.album_picnr),imagetype)
                filename = u'%s.%s' % (unicode(self.album_picnr),imagetype)

                save_path = self.album.folder_path
                # Tvinger Album til å lage mapper dersom de ikke finnes
                try:
                    os.stat(save_path)
                except:
                    self.album.save()
                
                # Lagrer thumbnail
                imagefile = open(os.path.join(save_path, filename), 'w')
                resizedImage.save(imagefile, img.format)
                imagefile.close()
                
                # Lagrer thumbnail
                imagefile = open(os.path.join(save_path, filename_thumb), 'w')
                thumbnail.save(imagefile, img.format)
                imagefile.close()
                    
                # Django bruker 'MEDIA_ROOT' som root for ImageFields:
                media_path = GALLERY_FOLDER + self.album.folder_path.split(GALLERY_DIR)[-1] + '/'
                self.picture = media_path + filename
                self.thumbnail = media_path + filename_thumb
                
                # Sletter det gamle bildet
                temp_path = img.filename
                os.remove(temp_path)
        
                super(Picture, self).save()


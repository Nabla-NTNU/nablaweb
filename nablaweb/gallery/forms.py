# -*- coding: utf-8 -*-

from django.forms import ModelForm,Form,CharField,Textarea,IntegerField,HiddenInput
from gallery.models import *

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        
class AlbumEditForm(Form):
    title = CharField(label='Tittel')
    description = CharField(label='Beskrivelse',widget=Textarea)
    album_id = IntegerField(label='album-id', widget=HiddenInput())
    
    def clean(self):
        cleaned_data = self.cleaned_data
        print cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        album_id = cleaned_data.get('album_id')
        
        # Sjekker om det finnes et album med den tittelen som er skrevet inn
        # som ikke er det albummet som holder på å bli endret
        similar_title = Album.objects.filter(title=title)
        if similar_title:
            if similar_title[0].id != album_id:
                self._errors["title"] = self.error_class([u'Det finnes et annet album med denne tittelen.'])
        print title
        if not title:
            self._errors["title"] = self.error_class([u'Albummet må ha en tittel.'])
        elif len(title) > 64:
            self._errors["title"] = self.error_class([u'Tittelen kan maks være 64 tegn.'])
        #super(AlbumEditForm,self).clean(self)
        if self._errors.get("description"): del self._errors["description"]
        return cleaned_data

class PictureForm(ModelForm):
    class Meta:
        model = Picture
        exclude = ('album','owner')
        
class PictureEditForm(ModelForm):
    class Meta:
        model = Picture
        fields = ('description',)

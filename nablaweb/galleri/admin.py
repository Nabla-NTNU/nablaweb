from gallery.models import *
from django.contrib import admin

class PictureAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tittel',      {'fields':['title']}),
        ('Beskrivelse', {'fields':['description']}),
        ('Bilde',       {'fields':['picture']}),
    ]

admin.site.register(Album)
admin.site.register(Picture, PictureAdmin)


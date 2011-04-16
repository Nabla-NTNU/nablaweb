from PIL import Image
import os
import hashlib
import StringIO

from django.template import Context, loader, RequestContext
from gallery.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.files import *
from django.core.urlresolvers import reverse
from django.conf import settings
#from django.template import RequestContext

#TODO: -Stripper ikke input paa noen forms, dvs man kan fortsatt bruke tekstinput til aa laste opp html, javascript ect.
#       (Update) Ser ut til at Django tar seg av dette likevel. 100% trygt?


""" Standard Views """

def index(request):
    album_list = Album.objects.all()
    return render_to_response('gallery/index.html', {'album_list': album_list})

def album(request, album_id):
    a = get_object_or_404(Album, pk=album_id)
    return render_to_response('gallery/album.html', {'album': a})


def picture_large(request, album_id, picture_number):
    album = get_object_or_404(Album, pk=album_id)
    album_pictures = album.picture_set.all()
    album_size = len(album_pictures)

    # "Oversetter" til den faktiske id-verdien til bildet
    picture_number = int(picture_number)
    picture_id = 0
    if (picture_number > 0 and picture_number <= album_size):
        picture_id = album_pictures[picture_number-1].id
    picture = get_object_or_404(Picture, pk=picture_id)

    return render_to_response('gallery/picture_large.html',
                             {'picture': picture, 'total': album_size,
                              'current': picture_number, 'album': album, 
                              'pic_list': album_pictures})


""" Opplasting av bilder """
#TODO: - (DONE)Sjekk om det er en ekte bildefil(PIL kan brukes)
#      - (DONE)virker album=current_album
#      - trenger en RequestContext hertitle=request.POST['title'] (fungerer ikke i 1.1.1)
#      - Fortsatt usikker paa hvorvidt jeg har oversett noen sikkerhetshull/bugs her.
#         Helt sikkert plenty av dem.
#      - (FIXED)Slaa sammen 'new_image_form' og 'manage_uploaded_image' + fjerne unodvendig kode

def new_image_form(request, album_id):
    current_album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        new_picture = Picture(title=request.POST['title'], description=request.POST['description'], album=current_album)
        try:
            new_picture.picture = request.FILES['picture']
            new_picture.save()
        except:
            return render_to_response('gallery/new_image_form.html', {
                                      'album': current_album, 'meta': new_picture, 'error_message': "Filen maa vaere et bilde" })
        else:
            return HttpResponseRedirect(reverse('gallery.views.album', args=(album_id,)))
    else:
        return render_to_response('gallery/new_image_form.html',
                                 {'album': current_album } )


""" Sletting av bilder """
#TODO: 
#        Et annet alternativ er A lagre dem i en 'angremappe', der filene ligger i
#        f.eks 10 dager f0r de slettes automatisk.

def delete_picture(request,album_id,picture_id):
    if int(picture_id):
        picture = get_object_or_404(Picture, pk=picture_id)
        picture.delete()
    a = get_object_or_404(Album, pk=album_id)
    return render_to_response('gallery/album.html', {'album': a, 'delete_mode':True})


""" Oppretting av nytt album """
def new_album(request):
    if request.method == 'POST':
        if request.POST['title']:
            album = Album(title = request.POST['title'], description = request.POST['description'])
            album.save()
            return HttpResponseRedirect(reverse('gallery.views.album', args=(album.id,)))
        else:
            return render_to_response('gallery/new_album_form.html',
                                      {'meta': request.POST['description'], 'error_message': "Du maa bestemme en tittel"})
    else:
        return render_to_response('gallery/new_album_form.html', )

""" Sletting av album """
def delete_album(request, album_id, confirmation):
    album_list = Album.objects.all()
    if int(album_id):
        album_delete = get_object_or_404(Album, pk=album_id)
        if not (str(confirmation) == '1'):
            return render_to_response('gallery/index.html', {'album_list': album_list, 'delete_mode':True, 
                                                             'album_delete': album_delete})
        else:
            # Trenger A overlagre bAde Album.delete() og Picture.delete() for A fA dette ordnet
            album_delete.delete()
            return HttpResponseRedirect(reverse('gallery.views.index', ))
    else:
        return render_to_response('gallery/index.html', {'album_list': album_list, 'delete_mode':True})
    

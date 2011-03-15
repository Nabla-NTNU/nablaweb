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

GALLERY_DIR = os.path.join(getattr(settings, 'MEDIA_ROOT', None),'gallery')

""" Innstillinger for opplastede bilders opplosning """

PICTURE_DIM = 720
PICTURE_DIM_THUMB = 128


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
#      - Slaa sammen 'new_image_form' og 'manage_uploaded_image' + fjerne unodvendig kode

def new_image_form(request, album_id):
    if request.method == 'POST':
        current_album = get_object_or_404(Album, pk=album_id)
        try:
            image = request.FILES['picture']
        except:
            return render_to_response('gallery/new_image_form.html', {
                                  'album': album, 'error_message': "Velg en fil f0r du trykker send" })
        else:
            new_picture = Picture(title=request.POST['title'], description=request.POST['description'], album=current_album )
            return manage_uploaded_image(request.FILES['picture'], new_picture, current_album)
    else:
        current_album = get_object_or_404(Album, pk=album_id)
        return render_to_response('gallery/new_image_form.html',
                                 {'album': current_album } )

# HAX
def manage_uploaded_image(picture, picture_object, album):
    imagefile = StringIO.StringIO(picture.read())
    try:
        img = Image.open(imagefile)
    except:
        return render_to_response('gallery/new_image_form.html', {
                                  'album': album, 'picture_meta': picture_object, 'error_message': "Filen maa vaere et bilde" })
    else:
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

        save_path = os.path.join(GALLERY_DIR,str(album.title))

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
        media_path = 'gallery/' + str(album.title) + '/'
        picture_object.picture = media_path + filename
        picture_object.thumbnail = media_path + filename_thumb
        picture_object.save()

        return HttpResponseRedirect(reverse('gallery.views.album', args=(album.id,)))


# En funksjon som returnerer skalerte verdier paa width og height
def scale_dimensions(width, height, lowest_side):
    if width > height:
        return ( lowest_side, int(height * lowest_side/float(width)) )
    else:
        return ( int(width * lowest_side/float(height)), lowest_side )

""" Sletting av bilder """

#TODO: -Slette filer, ikke bare django-objektet, evt flytte dem til en 'restemappe'
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

    

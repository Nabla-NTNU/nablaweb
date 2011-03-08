from django.template import Context, loader, RequestContext
from gallery.models import *
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404

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

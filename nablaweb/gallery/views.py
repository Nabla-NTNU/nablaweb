# -*- coding: utf-8 -*-

#from PIL import Image
#import os
#import hashlib
#import StringIO

from django.views.generic import DeleteView
from django.template import Context, loader, RequestContext
from gallery.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.files import *
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from gallery.forms import *


#TODO: -Stripper ikke input paa noen forms, dvs man kan fortsatt bruke tekstinput til aa laste opp html, javascript ect.
#       (Update) Ser ut til at Django tar seg av dette likevel. 100% trygt?


""" Standard Views """

def index(request):
    album_list = Album.objects.all()
    return render_to_response('gallery/index.html', {'album_list': album_list}, context_instance=RequestContext(request))

def album(request, *args, **kwargs):
    a = get_object_or_404(Album, pk=kwargs.get('album_id'))
    return render_to_response('gallery/album.html', {'album': a},context_instance=RequestContext(request))


def picture_large(request, *args, **kwargs):
    album = get_object_or_404(Album, pk=kwargs.get('album_id'))
    picture = get_object_or_404(Picture, pk=album.picture_set.get(album_picnr=kwargs.get('album_picnr')).id)
    picture_set = album.picture_set.all()
    
    # Finner det forrige og neste bildet:
    for i in range(0,len(picture_set)):
        if picture_set[i].id == picture.id:
            if i: previous_picture = picture_set[i-1]
            else: previous_picture = picture_set[len(picture_set)-1]
            if (len(picture_set) > i+1): next_picture = picture_set[i+1]
            else: next_picture = picture_set[0]
    """              
    next_picture = album.picture_set.filter(album_picnr__in=range(picture.album_picnr + 1, picture_set[len(picture_set) - 1].album_picnr + 1))
    if next_picture:
        next_picture = next_picture[0]
    else:
        next_picture = picture_set[0]            
    for pic in picture_set:
        if pic.album_picnr == picture.album_picnr:
            previous_picture = 
    previous_picture = album.picture_set.filter(album_picnr__in=range(0,picture.album_picnr)) 
    if previous_picture:
        previous_picture = previous_picture[len(previous_picture)-1]
    else:
        previous_picture = picture_set[len(picture_set)-1]
    """
    picture.increment_number_of_hits()
    return render_to_response('gallery/picture_large.html',
                             {'picture': picture, 'album': album, 'next_picture':next_picture, 'previous_picture':previous_picture},context_instance=RequestContext(request))




""" NYE VIEWS ALPHA """

"""##############################################################################"""

""" ___ADD ALBUM___ """
@login_required
def add_album(request):
    if (request.method == 'POST'):
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = Album(title=form.cleaned_data['title'],description=form.cleaned_data['description'])
            album.save()
            return HttpResponseRedirect(reverse('gallery.views.album', args=(album.id,)))
    else:
        form = AlbumForm()
    return render_to_response('gallery/add_album.html', {'form': form,}, context_instance=RequestContext(request))
    
""" ___EDIT ALBUM___ """
@login_required
def edit_album(request, *args, **kwargs):
    album = get_object_or_404(Album, pk=kwargs.get('album_id'))
    if (request.method == 'POST'):
        form = AlbumEditForm(request.POST)
        print form.base_fields['title']
        if form.is_valid():
            album.title = form.cleaned_data['title']
            if form.cleaned_data.get('description'):
                album.description = unicode(form.cleaned_data.get('description'))
            else:
                album.description = u''
            album.save()
            return HttpResponseRedirect(reverse('gallery.views.album', args=(album.id,)))
    else:
        form = AlbumEditForm({'title':album.title,'description':album.description,'album_id':album_id})
    return render_to_response('gallery/edit_album.html', {'form': form,'album':album}, context_instance=RequestContext(request))
    
""" ___DELETE ALBUM___ """
class AlbumDeleteView(DeleteView):
    model = Album
    context_object_name = 'album'
    
    def get_success_url(self):
        return reverse('gallery.views.index')

""" ___ADD PICTURE___ """
@login_required
def add_picture(request,*args,**kwargs):
    album_id = kwargs.get('album_id')
    current_album = get_object_or_404(Album, pk=album_id)
    if (request.method == 'POST'):
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            new_picture = Picture(description=form.cleaned_data.get('description'), picture=form.cleaned_data['picture'],owner=request.user,album=current_album)
            new_picture.save()
            return HttpResponseRedirect(reverse('gallery.views.album', args=(current_album.id,)))
    else:
        form = PictureForm()
    return render_to_response('gallery/add_picture.html', {'form': form,'album':current_album}, context_instance=RequestContext(request))

""" ___EDIT PICTURE___ """
@login_required
def edit_picture(request, *args, **kwargs):
    album = get_object_or_404(Album, pk=kwargs.get('album_id'))
    picture = get_object_or_404(Picture, pk=album.picture_set.get(album_picnr=kwargs.get('picture_id')).id)
    if (request.method == 'POST'):
        form = PictureEditForm(request.POST)
        if form.is_valid():
            picture.description = form.cleaned_data.get('description')
            picture.save()
            return HttpResponseRedirect(reverse('gallery.views.picture_large', args=(album.id,picture.album_picnr,)))
    else:
        form = PictureEditForm({'description':picture.description})
    return render_to_response('gallery/edit_picture.html', {'form':form, 'album':album, 'picture':picture}, context_instance=RequestContext(request))
    
""" ___DELETE PICTURE___ """
@login_required
def delete_picture(request, *args, **kwargs):
    album = get_object_or_404(Album, pk=kwargs.get('album_id'))
    picture = get_object_or_404(Picture, pk=album.picture_set.get(album_picnr=kwargs.get('picture_id')).id)
    if (request.method == 'POST'):
        if (request.POST['confirmation'] == 'Ja'):
            picture.delete()
        return HttpResponseRedirect(reverse('gallery.views.album', args=(album.id,)))
    else:
        return render_to_response('gallery/delete_picture.html', {'picture':picture, 'album':album}, context_instance=RequestContext(request))   
         

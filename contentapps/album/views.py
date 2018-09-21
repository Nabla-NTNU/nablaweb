"""
Views for album app
"""
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Album


class AlbumList(ListView):
    """
    List of publically visible albums
    """
    model = Album
    context_object_name = "albums"
    template_name = "album/album_list.html"
    paginate_by = 10
    queryset = Album.objects.exclude(visibility='h').order_by('-created_date')


class PermissionToSeeAlbumMixin:
    """
    Mixin for checking if the user is allowed to view the album

    Assumes that the public key of the album
    is supplied as a keyword argument called 'pk' from the urlpatterns.

    Redirect to login if user is not allowed to view the album.
    """
    def dispatch(self, request, *args, **kwargs):
        """View dispatch"""
        album = Album.objects.get(pk=kwargs['pk'])
        allowed_to_view_album = album.is_visible(request.user)
        if not allowed_to_view_album:
            return redirect('auth_login')
        return super().dispatch(request, *args, **kwargs)


class AlbumOverview(PermissionToSeeAlbumMixin, DetailView):
    """
    Show an album with all images in the album if the user is allowed to view them.
    """
    model = Album
    context_object_name = "album"
    template_name = "album/album_overview.html"


class AlbumImageView(PermissionToSeeAlbumMixin, TemplateView):
    """
    View a single album image with links to next and previous image in the album.
    """

    template_name = "album/album_image.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = get_object_or_404(Album, pk=kwargs['pk'])

        images = context['album'].images.order_by('num').all()
        paginator = Paginator(images, 1)
        context['page_obj'] = paginator.page(kwargs['num'])

        if context['page_obj'].object_list:
            context['image'] = context['page_obj'].object_list[0]

        return context

"""
Views for album app
"""
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from .models import Album


class AlbumList(ListView):
    """
    List of publically visible albums
    """

    model = Album
    context_object_name = "albums"
    template_name = "album/album_list.html"
    paginate_by = 12
    queryset = (
        Album.objects.filter(level=0).exclude(visibility="h").order_by("-created_date")
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_user"] = self.request.user.is_authenticated
        return context


class PermissionToSeeAlbumMixin:
    """
    Mixin for checking if the user is allowed to view the album

    Assumes that the public key of the album
    is supplied as a keyword argument called 'pk' from the urlpatterns.

    Redirect to login if user is not allowed to view the album.
    """

    def dispatch(self, request, *args, **kwargs):
        """View dispatch"""
        album = get_object_or_404(Album, pk=kwargs["pk"])
        allowed_to_view_album = album.is_visible(request.user)
        if not allowed_to_view_album:
            return redirect("auth_login")
        return super().dispatch(request, *args, **kwargs)


class AlbumOverview(PermissionToSeeAlbumMixin, DetailView):
    """
    Show an album with all images in the album if the user is allowed to view them.
    """

    model = Album
    context_object_name = "album"
    template_name = "album/album_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["children"] = self.object.get_children().exclude(visibility="h")
        else:
            context["children"] = self.object.get_children().exclude(visibility="h")
        context["is_user"] = self.request.user.is_authenticated
        context["ancestors"] = self.object.get_ancestors(
            ascending=False, include_self=True
        )
        context["overview_url"] = reverse("albums")
        return context


class AlbumImageView(PermissionToSeeAlbumMixin, TemplateView):
    """
    View a single album image with links to next and previous image in the album.
    """

    template_name = "album/album_image.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["album"] = get_object_or_404(Album, pk=kwargs["pk"])

        images = context["album"].images.order_by("num").all()
        paginator = Paginator(images, 1)
        page = self.request.GET.get("page")
        if page is not None:
            context["page_obj"] = paginator.get_page(page)
        else:
            try:
                context["page_obj"] = paginator.get_page(kwargs["num"])
            except EmptyPage:
                raise Http404("Bildet finnes ikke")

        if context["page_obj"].object_list:
            context["image"] = context["page_obj"].object_list[0]
        context["overview_url"] = reverse("albums")

        context["admin_links"] = [
            {
                "name": "Endre Album",
                "font_awesome": "cog",
                "url": reverse("admin:album_album_change", args=[context["album"].id]),
            }
        ]

        return context

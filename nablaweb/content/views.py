from django.views.generic import TemplateView, ListView
from .models import Album


class AlbumOverview(ListView):
    model = Album
    context_object_name = "albums"
    template_name = "content/album_overview.html"


class AlbumView(TemplateView):

    def get_context_data(self, **kwargs):
        context = []
        num = kwargs['num']
        context['album'] = Album.objects.get({'id':  kwargs['pk']})
        context['image'] = album.images[num]

        return context

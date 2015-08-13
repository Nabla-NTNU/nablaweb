
from content.models import Archive, ArchiveEntry
from django.views.generic import ListView, DetailView


class ArchiveView(ListView):

    template_name = "content/archive.html"
    context_object_name = "entry_list"

    def __init__(self, **kwargs):
        super(ArchiveView, self).__init__(**kwargs)
        name = kwargs.get('archive')
        self.archive = Archive.objects.get(name=name)

    def get_queryset(self):
        return self.archive.entries


class ArchiveEntryView(DetailView):
    model = ArchiveEntry

    template_name = "content/archive_entry.html"

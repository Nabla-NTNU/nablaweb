from content.views import ContentListView, ContentDetailView, ContentDeleteView
from nabladet.models import Nablad

class NabladDetailView(ContentDetailView):
    model = Nablad

class NabladListView(ContentListView):
    model = Nablad


from news.views import NewsListView, NewsDetailView, NewsDeleteView
from nabladet.models import Nablad

class NabladDetailView(NewsDetailView):
    model = Nablad

class NabladListView(NewsListView):
    model = Nablad


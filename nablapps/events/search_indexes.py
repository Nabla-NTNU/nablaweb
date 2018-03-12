import datetime
from haystack import indexes
from .models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publication_date__lte=datetime.datetime.now())


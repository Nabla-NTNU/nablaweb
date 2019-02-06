"""
Haystack search indexes for events-app
"""
from datetime import datetime
from haystack import indexes
from .models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    """Search index for Event-model"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

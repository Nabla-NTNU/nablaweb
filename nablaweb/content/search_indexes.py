from haystack import indexes
from content.models import Content
import datetime

class ContentIndex(indexes.SearchIndex, indexes.Indexable):
    headline = indexes.CharField(model_attr='headline')
    lead_paragraph = indexes.CharField(model_attr='lead_paragraph')
    body = indexes.CharField(model_attr='body')
    created_date = indexes.DateTimeField(model_attr='created_date')
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Content
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created_date__lte=datetime.datetime.now())

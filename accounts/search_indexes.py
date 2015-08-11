from haystack import indexes
from accounts.models import NablaUser


class NablaUserIndex(indexes.SearchIndex, indexes.Indexable):
    username = indexes.CharField(model_attr='username')
    about = indexes.CharField(model_attr='about')
    cell_phone = indexes.CharField(model_attr='cell_phone')
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return NablaUser
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)

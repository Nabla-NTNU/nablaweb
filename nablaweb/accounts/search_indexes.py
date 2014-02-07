from haystack import indexes
from accounts.models import UserProfile
import datetime

class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
    user = indexes.CharField(model_attr='user')
    about = indexes.CharField(model_attr='about')
    cell_phone = indexes.CharField(model_attr='cell_phone')
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return UserProfile
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

"""
Haystack search indexes for blog app

Will be imported by haystack if haystack is used.
"""
from haystack import indexes  # pylint: disable=E0401

from .models import BlogPost


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Search index for blog entries
    """

    title = indexes.CharField(model_attr="title")
    content = indexes.CharField(model_attr="content")
    created_date = indexes.DateTimeField(model_attr="created_date")
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """Return corresponding model"""
        return BlogPost

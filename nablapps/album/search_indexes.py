"""
Haystack search indexes for album app

Will be imported by haystack if haystack is used.
"""
from haystack import indexes  # pylint: disable=E0401

from .models import Album


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Search index for entire albums
    """

    title = indexes.CharField(model_attr="title")
    created_date = indexes.DateTimeField(model_attr="created_date")
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """Return corresponding model"""
        return Album

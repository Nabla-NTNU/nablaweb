
from django.test import TestCase
from content.models import Album


class AlbumTest(TestCase):

    def test_album_creation(self):
        self.album = Album()
        self.album.title = "Some album"
        self.album.visibillity = 'p'
        self.album.save()

    def test_album_loaded(self):
        self.response = self.client.get(
            self.album.get_absolute_url()
        )

        self.assertIn(self.album.title, self.response)

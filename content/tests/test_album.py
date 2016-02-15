from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()

from content.models import Album


class AlbumTest(TestCase):

    def test_album_creation(self):
        self.album = Album()
        self.album.title = "Some album"
        self.album.visibility = 'p'
        self.album.save()

        self.response = self.client.get(
            self.album.get_absolute_url()
        )

        self.assertIn(self.album.title.encode(), self.response.content)


class AlbumVisibilityTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(title="Some album")

    def test_public_album_is_visible(self):
        self.album.visibility = 'p'
        self.album.save()
        self.assertTrue(self.album.is_visible())

    def test_hidden_album_not_visible(self):
        self.album.visibility = 'h'
        self.album.save()
        self.assertFalse(self.album.is_visible())

    def test_user_visible_no_user_supplied(self):
        self.album.visibility = 'u'
        self.album.save()
        self.assertFalse(self.album.is_visible())

    def test_user_visible_user_supplied(self):
        self.album.visibility = 'u'
        self.album.save()
        user = UserModel.objects.create(username="user1")
        self.assertTrue(self.album.is_visible(user=user))

    def test_unknown_visibility(self):
        self.album.visibility = '#'
        self.album.save()
        self.assertFalse(self.album.is_visible())

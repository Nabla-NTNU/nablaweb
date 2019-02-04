from django.test import TestCase
from django.contrib.auth import get_user_model
from nablapps.album.models import Album


UserModel = get_user_model()


class AlbumTest(TestCase):

    def test_album_creation(self):
        album = Album()
        album.title = "Some album"
        album.visibility = 'p'
        album.save()

        response = self.client.get(
            album.get_absolute_url()
        )

        self.assertIn(album.title.encode(), response.content)


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

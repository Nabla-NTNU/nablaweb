from django.test import TestCase

from likes.models import toggle_like, get_like_count

from .base import User, create_test_object


class LikeCountTest(TestCase):
    def setUp(self):
        self.users = [User.objects.create(username="user{}".format(i)) for i in range(10)]
        self.object = create_test_object()

    def assertNLikes(self, n):
        self.assertEqual(get_like_count(self.object), n)

    def createNLikes(self, n):
        for user in self.users[:n]:
            toggle_like(self.object, user)

    def test_no_likes(self):
        self.assertNLikes(0)

    def test_one_like(self):
        self.createNLikes(1)
        self.assertNLikes(1)

    def test_five_likes(self):
        self.createNLikes(5)
        self.assertNLikes(5)

    def test_ten_likes(self):
        self.createNLikes(10)
        self.assertNLikes(10)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from nablapps.likes.models import user_likes

User = get_user_model()


def create_test_object():
    if "dummyapp" in settings.INSTALLED_APPS:
        from nablapps.likes.tests.dummyapp import DummyModel
        object = DummyModel.objects.create()
    else:
        from django.contrib.auth.models import Group
        object = Group.objects.create(name="Yo")
    return object


class BaseLikeTest(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "mypassword_is_very_cool!with_numbers5643245"
        self.user = User.objects.create(username=self.username, email="a@b.c")
        self.user.set_password(self.password)
        self.user.save()
        self.object = create_test_object()

    def assertUserLikes(self, user, object):
        self.assertTrue(user_likes(object, user), "{} should like {}".format(user, object))

    def assertNotUserLikes(self, user, object):
        self.assertFalse(user_likes(object, user), "{} should not like {}".format(user, object))


class BaseViewTest(BaseLikeTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("toggle_like")
        ct = ContentType.objects.get_for_model(self.object)
        self.post_data = {'contenttypeId': ct.id, 'objectId': self.object.id}

    def login(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        assert logged_in

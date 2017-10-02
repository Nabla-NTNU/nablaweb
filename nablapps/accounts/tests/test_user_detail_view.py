from django.test import TestCase
from django.core.urlresolvers import reverse
from nablapps.accounts.models import NablaUser


class TestUserDetail(TestCase):

    def setUp(self):
        self.user1 = NablaUser.objects.create_user(username="user1")
        self.user2_password = "hallo"
        self.user2 = NablaUser.objects.create_user(
            username="user2", password=self.user2_password)

    def test_logged_in_user_can_view_profile(self):
        self.client.login(username=self.user2.username, password=self.user2_password)
        profile_url = reverse("member_profile", kwargs={"username": self.user1.username})
        response = self.client.get(profile_url)
        self.assertContains(response, self.user2.username)

    def test_anonymous_user_cannot_view_profile(self):
        url = reverse("member_profile", kwargs={"username": self.user1.username})
        response = self.client.get(url)
        self.assertRedirects(response, "/login/?next={}".format(url))

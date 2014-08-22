"""
Tester for accounts-appen
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .views import UserDetailView


class TestUserDetail(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1")
        self.user2_password = "hallo"
        self.user2 = User.objects.create_user(username="user2", password=self.user2_password)

    def test_logged_in_user_can_view_profile(self):
        self.client.login(username=self.user2.username, password=self.user2_password)
        response = self.client.get(reverse("member_profile", kwargs={"username": self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2.username, response.content)

    def test_anonymous_user_cannot_view_profile(self):
        url = reverse("member_profile", kwargs={"username": self.user1.username}) 
        response = self.client.get(url)
        self.assertRedirects(response, "/login/?next={}".format(url))








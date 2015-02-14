"""
Tester for accounts-appen
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from accounts.models import NablaUser

class TestUserDetail(TestCase):

    def setUp(self):
        self.user1 = NablaUser.objects.create_user(username="user1")
        self.user2_password = "hallo"
        self.user2 = NablaUser.objects.create_user(username="user2", password=self.user2_password)

    def test_logged_in_user_can_view_profile(self):
        self.client.login(username=self.user2.username, password=self.user2_password)
        response = self.client.get(reverse("member_profile", kwargs={"username": self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2.username, response.content)

    def test_anonymous_user_cannot_view_profile(self):
        url = reverse("member_profile", kwargs={"username": self.user1.username}) 
        response = self.client.get(url)
        self.assertRedirects(response, "/login/?next={}".format(url))

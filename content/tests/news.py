# -*- coding: utf-8 -*-
"""
Tester for News-appen til Nablaweb
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from content.models.news import News

User = get_user_model()


class NewsDetailViewTest(TestCase):

    def setUp(self):
        # Lager en ny nyhet som brukes i testing
        self.news = News()
        self.news.headline = 'Overskrifta er kul'
        self.user = User.objects.create(
            first_name=u'Oystein',
            last_name=u'Hiasen',
            username='hiasen_test')
        self.lead_paragraph = "Dette er en veldig spennende nyhet som du bare må lese!"
        self.body = "Haha, jeg lurte deg. Det er ikke så spennende alikevel."
        self.news.created_by = self.user
        self.news.save()

        # Prøver å laste inn siden til nyheten og tar vare på resultatet
        self.response = self.client.get(
            self.news.get_absolute_url()
        )

    def test_headline_is_on_page(self):
        self.assertIn(self.news.headline.encode(), self.response.content)

    def test_lead_paragraph_is_on_page(self):
        self.assertIn(self.news.lead_paragraph.encode(), self.response.content)

    def test_body_is_on_page(self):
        self.assertIn(self.news.body.encode(), self.response.content)

    def test_publisher_is_on_page(self):
        self.assertIn(self.user.get_full_name().encode(), self.response.content)

# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse

from content.models import Event, News


class MyTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            headline="Yo",
        )

    def test_yo(self):
        self.assertEqual(self.event.headline, "Yo")

    def test_get_news_dont_change_content_type(self):
        event_content_type = self.event.content_type
        url = reverse("news_detail", kwargs={"pk": self.event.pk, "slug": "asdfasdf"})
        self.client.get(url)
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(event.content_type, event_content_type, "Contenttype should be unchanged when loading news")

    def test_get_news_redirect_if_subclass(self):
        url_to_redirect_to = self.event.get_absolute_url()
        url = reverse("news_detail", kwargs={"pk": self.event.pk, "slug": "asdfasdf"})
        response = self.client.get(url)
        self.assertRedirects(response, url_to_redirect_to)

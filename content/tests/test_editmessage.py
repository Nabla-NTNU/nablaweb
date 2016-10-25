from django.test import TestCase
from django.contrib.auth.models import User

from django_nyt.models import Subscription, Notification

from content.models.news import News


class EditTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(headline='Hei')
        self.user = User.objects.create(username='jaja')


class SubscriptionTest(EditTest):
    def test_subscription(self):
        self.assertFalse(Subscription.objects.all())
        self.news.subscribe_to_changes(self.user)
        self.assertTrue(Subscription.objects.all())

    def test_watch_field_has_changed(self):
        pass


class NotificationTest(EditTest):
    def setUp(self):
        super().setUp()
        self.news = News.objects.get(id=self.news.id)
        self.news.subscribe_to_changes(self.user)

    def test_notify(self):
        self.assertFalse(Notification.objects.all())
        self.news.notify('Hello this is a message')
        self.assertTrue(Notification.objects.all())

    def test_edit(self):
        self.assertFalse(Notification.objects.all())
        self.news.headline = 'new headline'
        self.news.save()
        self.assertTrue(Notification.objects.all())

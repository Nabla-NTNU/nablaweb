from django.test import TestCase
from django.contrib.auth import get_user_model

from django_nyt.models import Subscription, Notification

from contentapps.news.models import News

UserModel = get_user_model()


class EditTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(headline='Hei')
        self.user = UserModel.objects.create(username='jaja')


class SubscriptionTest(EditTest):
    def test_subscription(self):
        self.assertFalse(Subscription.objects.all())
        self.news.subscribe_to_changes(self.user)
        self.assertTrue(Subscription.objects.all())

    def test_watch_field_has_changed(self):
        self.news._save_watch_fields_as_old_fields()
        self.news.headline = 'asfasdfasdfasdfasdfasdf'
        self.assertTrue(self.news._watch_fields_has_changed())


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

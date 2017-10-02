from django.test import TestCase
from nablapps.poll.models import Poll
from .utils import create_poll


class CurrentPollTest(TestCase):

    def setUp(self):
        self.first_poll = create_poll(u"Hvem er du?")
        self.second_poll = create_poll(u"Hvor kommer verden fra?")

    def assert_is_current_poll(self, poll):
        self.assertEqual(poll, Poll.objects.current_poll())

    def test_last_created_poll_is_current(self):
        self.assert_is_current_poll(self.second_poll)

    def test_set_is_current(self):
        self.first_poll.is_current = True
        self.first_poll.save()

        # Get second_poll again because it has been updated
        second_poll = Poll.objects.get(pk=self.second_poll.pk)

        self.assert_is_current_poll(self.first_poll)
        self.assertFalse(second_poll.is_current)

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from poll.context_processors import poll_context

from .utils import create_poll


class TestContextProcessor(TestCase):
    """Test the poll_context context processor"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_no_poll(self):
        """An empty context is supplied if there is no current poll."""
        context = poll_context(self.factory.get("/"))
        self.assertDictEqual(context, {})

    def test_poll_exist(self):
        poll = create_poll("What?")

        request = self.factory.get("/")
        request.user = AnonymousUser()

        context = poll_context(request)
        self.assertEqual(poll, context["poll"])
        self.assertFalse(context["poll_has_voted"])
        self.assertEqual(poll.get_total_votes(), context["poll_total_votes"])

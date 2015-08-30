from django.test import TestCase
from django.http import HttpRequest

from nablaweb.context_processors import get_primary_dir


class TestPrimaryDir(TestCase):
    """Class for testing the primary_dir context processor"""
    def test_batman(self):
        """Test batman as primary dir."""
        request = HttpRequest()
        request.path = "/batman/cakes"
        context = get_primary_dir(request)

        self.assertEqual(context["primary_dir"], "batman")
        self.assertEqual(context["primary_dir_slashes"], "/batman/")

    def test_no_primary_dir(self):
        request = HttpRequest()
        request.path = "/"
        context = get_primary_dir(request)

        self.assertEqual(context["primary_dir"], "")
        self.assertEqual(context["primary_dir_slashes"], "/")

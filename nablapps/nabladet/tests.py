"""
Tests for nablad app
"""
import os
from shutil import copyfile, rmtree

from django.conf import settings
from django.test import TestCase, tag

from .pdfthumbnailer import thumbnail_pdf


class ThumbnailerTestCase(TestCase):
    """
    TestCase for testing creation of thumbnails of pdfs.
    """

    def setUp(self):
        source = os.path.join(os.path.dirname(__file__), "test_static/test_nabla.pdf")
        self.test_dir = os.path.join(
            settings.PROTECTED_MEDIA_ROOT, "thumbnails/nabladet/test"
        )
        os.makedirs(self.test_dir)
        self.test_pdf = os.path.join(self.test_dir, "test_nabla.pdf")
        copyfile(source, self.test_pdf)

    # Indicate that this test needs imagemagick to run. This allows
    # excluding it on platforms that do not have it installed.
    @tag("needs_imagemagick")
    def test_thumbnailer(self):
        """
        Did the thumbnail creation work?

        This will fail if ImageMagick is not correctly installed
        """
        test_thumbnail = thumbnail_pdf(self.test_pdf)
        assert os.path.isfile(test_thumbnail), (
            "Did not create thumbnail. This test requires ImageMagick to run. "
            "If you do not have it installed, you can skip this test by passing "
            "`--exclude-tag=needs_imagemagick` to `manage.py test`"
        )

    def tearDown(self):
        rmtree(self.test_dir, ignore_errors=True)

from django.test import TestCase
from django.conf import settings

from .pdfthumbnailer import thumbnail_pdf

import os


class ThumbnailerTestCase(TestCase):

    def setUp(self):
        self.test_pdf = os.path.join(settings.STATIC_ROOT, 'nabladet/test_nabla.pdf')

    def test_thumbnailer(self):
        self.test_thumbnail = thumbnail_pdf(self.test_pdf)

    def tearDown(self):
        os.remove(self.test_thumbnail)

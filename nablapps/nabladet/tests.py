from django.test import TestCase

from .pdfthumbnailer import thumbnail_pdf

import os


class ThumbnailerTestCase(TestCase):

    def setUp(self):
        self.test_pdf = os.path.join(os.path.dirname(__file__), 'test_static/test_nabla.pdf')

    def test_thumbnailer(self):
        self.test_thumbnail = thumbnail_pdf(self.test_pdf)

    def tearDown(self):
        os.remove(self.test_thumbnail)

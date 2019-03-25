from django.test import TestCase
from django.conf import settings

from .pdfthumbnailer import thumbnail_pdf

import os
from shutil import copyfile


class ThumbnailerTestCase(TestCase):

    def setUp(self):
        source = os.path.join(os.path.dirname(__file__), 'test_static/test_nabla.pdf')
        self.dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails/nabladet/test')
        os.mkdir(self.dir)
        self.test_pdf = os.path.join(self.dir, 'test_nabla.pdf')
        copyfile(source, self.test_pdf)

    def test_thumbnailer(self):
        self.test_thumbnail = thumbnail_pdf(self.test_pdf)

    def tearDown(self):
        os.remove(self.test_thumbnail)
        os.remove(self.test_pdf)
        os.rmdir(self.dir)

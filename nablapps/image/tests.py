"""
Tests for image app
"""

# pylint: disable=C0111
from django.test import TestCase

from nablapps.image.markdownprocessing import content_markdown
from nablapps.image.models import ContentImage


class BaseContentImageTest(TestCase):
    def setUp(self):
        ContentImage.objects.bulk_create(
            [ContentImage(file=f"image{i}.jpg") for i in range(10)]
        )


class ContentImageTest(BaseContentImageTest):
    def test_get_image(self):
        image = ContentImage.objects.first()
        self.assertIsNotNone(image)


class MarkdownProcessTest(BaseContentImageTest):
    def setUp(self):
        super().setUp()
        self.first_image = ContentImage.objects.get(id=1)

    def test_empty_string(self):
        self.assertEqual(content_markdown(""), "")

    def test_simple_image(self):
        result = content_markdown("[image:1]")
        self.assertIn(self.first_image.file.name, result)
        self.assertNotIn("[image:1]", result)

    def test_nonexistant_image(self):
        content_markdown("[image:20000000]")

    def test_multiple_images(self):
        result = content_markdown("[image:1]\n[image:2]\n[image:3]")
        for i in range(1, 4):
            self.assertIn(ContentImage.objects.get(id=i).file.name, result)

    def test_small_image(self):
        result = content_markdown("[image:1 size:small]")
        self.assertIn(self.first_image.file.name, result)
        self.assertIn("350px", result)

    def test_large_image(self):
        result = content_markdown("[image:1 size:large]")
        self.assertIn(self.first_image.file.name, result)
        self.assertIn("500px", result)

    def test_full_image(self):
        result = content_markdown("[image:1 size:full]")
        self.assertIn(self.first_image.file.name, result)
        self.assertIn("100%", result)

    def test_invalid_size(self):
        """Invalid sizes are not processed"""
        self.assertIn(
            "[image:1 size:invalidsize]", content_markdown("[image:1 size:invalidsize]")
        )

    def test_left_align(self):
        result = content_markdown("[image:1 align:left]")
        self.assertIn(self.first_image.file.name, result)
        self.assertIn("left", result)

    def test_right_align(self):
        result = content_markdown("[image:1 align:right]")
        self.assertIn(self.first_image.file.name, result)
        self.assertIn("right", result)

    def test_invalid_align(self):
        md_input = "[image:1 align:invalid]"
        result = content_markdown(md_input)
        self.assertIn(md_input, result)

    def test_align_and_size(self):
        result = content_markdown("[image:1 align:right size:full]")
        self.assertIn(self.first_image.file.name, result)
        self.assertIn("right", result)
        self.assertIn("100%", result)

    def test_caption(self):
        result = content_markdown("[image:1]\n    This is a caption.")
        self.assertIn("This is a caption.", result)

    def test_multiline_caption(self):
        result = content_markdown(
            "[image:1]\n    This is a\n    multiline\n    caption"
        )
        self.assertIn("This is a\nmultiline\ncaption", result)

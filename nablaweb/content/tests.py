# -*- coding: utf-8 -*-
"""
Tester for Content.

Inneholder tester for den abstrakte Content-modellen.
"""

from django.test import TestCase
from django.contrib.sites.models import Site
from django_comments.models import Comment
from datetime import datetime

from .models import Content, Album, AlbumImage

# Content er en abstrakt klasse.
# Lager derfor en indentisk underklasse av Content for å teste den.
class ConcreteContent(Content):
    pass


class ContentModelTest(TestCase):

    def test_saving_and_retrieving_content(self):
        first_content = ConcreteContent()
        first_content.save()
        second_content = ConcreteContent()
        second_content.save()

        retrieved_content = ConcreteContent.objects.all()[0]

        self.assertEqual(first_content, retrieved_content)
        self.assertNotEqual(second_content, retrieved_content)

    def test_deleting_content(self):
        content = ConcreteContent()
        content.save()

        self.assertEqual(ConcreteContent.objects.count(), 1)

        content.delete()

        self.assertEqual(ConcreteContent.objects.count(), 0)

    def test_deleting_content_with_comment(self):
        first_content = ConcreteContent()
        first_content.save()
        second_content = ConcreteContent()
        second_content.save()

        self._add_comment(first_content)
        self._add_comment(first_content)
        self._add_comment(second_content)

        first_content.delete()
        self.assertEqual(Comment.objects.count(), 1, 'Comments have not been deleted.')
        self.assertEqual(Comment.objects.all()[0].content_object, second_content,
                'The wrong comment has been deleted along with some content.')

    def _add_comment(self, content):
        ## Lag en kommentar tilhørende content-objektet
        comment = Comment()
        comment.content_type = content.content_type
        comment.object_pk = content.id
        comment.content_object = content
        site = Site.objects.all()[0]
        comment.site_id = site.id
        comment.save()

    def test_editing_content(self):
        content = ConcreteContent()
        content.save()
        import time
        time.sleep(2)
        content.save()

        self.assertTrue(content.has_been_edited())

    def test_created_date(self):
        before = datetime.now()
        content = ConcreteContent()
        content.save()
        after = datetime.now()

        self.assertGreaterEqual(content.created_date, before)
        self.assertLessEqual(content.created_date, after)


class AlbumTest(TestCase):

    def test_album_creation(self):
        album = Abum()
        album.title = "Some album"
        album.save()

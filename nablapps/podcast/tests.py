from django.test import TestCase
from .models import Podcast, Season


class PodcastBaseTests(TestCase):

    def test_creation(self):
        season = Season()
        season.number = 1
        season.save()
        podcast = Podcast()
        podcast.title = "Test"
        podcast.season = season
        podcast.description = "Description of podcast"
        podcast.save()

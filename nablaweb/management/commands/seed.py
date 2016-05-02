# Custom seed script for nablaweb
from accounts.models import NablaUser as User
from loremipsum import get_sentences, generate_paragraph
from content.models.news import News
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
        help = 'Puts data into the database'

        def handle(self, *args, **options):

            if not settings.DEBUG:
                raise Exception("Trying to seed in production.")

            User.objects.update_or_create(
                    username='admin',
                    password='admin',
                    email='admin@stud.ntnu.no'
                    )


            for i in range(0, 10):
                News.objects.update_or_create(
                        headline=get_sentences(1),
                        body='\n\n'.join([generate_paragraph()[2] for j in range(0, 4)]),
                        lead_paragraph=generate_paragraph()
                        )




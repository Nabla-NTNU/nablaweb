# Custom seed script for nablaweb
from accounts.models import NablaUser as User
from loremipsum import get_sentences, generate_paragraph
from content.models.news import News
from content.models.events import Event
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime as dt


def g():
    return '\n\n'.join([generate_paragraph(1)[2] for j in range(0, 4)])
    
def s():
    return get_sentences(1)

class Command(BaseCommand):
        help = 'Puts data into the database'

        def handle(self, *args, **options):
            
            if not settings.DEBUG:
                raise Exception("Trying to seed in production.")
            
            User.objects.all().delete()
            User.objects.update_or_create(
                    username='admin',
                    password='admin',
                    email='admin@stud.ntnu.no'
                    )
            
            for i in range(100):
                username = "komponent%d" % (i)
                User.objects.update_or_create(
                        username=username,
                        password='password',
                        email=username+'@stud.ntnu.no',
                        about=generate_paragraph(4)[2]
                        )

            News.objects.all().delete()

            for i in range(0, 10):
                News.objects.create(
                        headline=s(),
                        body=g(),
                        lead_paragraph=generate_paragraph()
                        )


            for i in range(10):
                Event.objects.create(
                    headline=s(),
                    body=g(),
                    lead_paragraph=g(),
                    short_name=g()
                )





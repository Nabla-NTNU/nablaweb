"""
Custom seed script for nablaweb
"""
import random
from datetime import datetime as dt, timedelta as td
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Factory
from nablapps.accounts.models import NablaUser as User, FysmatClass, NablaGroup
from nablapps.events.models import Event
from nablapps.news.models import NewsArticle


fake = Factory.create('no_NO')


def g():
    return fake.text()

    
def s():
    return fake.sentence()


class Command(BaseCommand):
    help = 'Puts data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            dest='delete',
            default=True,
            help='Delete existing data',
        )

    def handle(self, *args, **options):
        
        if not settings.DEBUG:
            raise Exception("Trying to seed in production.")
        
        delete = options['delete']
        print("Deleting old entries: " + str(delete))
        
        if delete:
            User.objects.all().delete()
        
        print("Creating superuser admin")
        User.objects.create_user(
            username='admin',
            password='admin',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            email='admin@stud.ntnu.no',
            about=fake.text(),
            birthday=fake.date_time_between_dates(
                datetime_start=None,
                datetime_end=None,
                tzinfo=None),
            is_superuser=True,
            is_staff=True
        )

        if delete:
            FysmatClass.objects.all().delete()

        count = random.randint(7, 10)
        print("Creating %d FysmatClasses" % count)
        year = dt.now().year
        classes = [
            FysmatClass.objects.create(
                starting_year=year-i,
                name="kull%d" % (year-i)
            )
            for i in range(count)
        ]
        
        if delete:
            NablaGroup.objects.all().delete()

        count = random.randint(5, 10)
        print("Creating %d NablaGroups" % count)
        ngroups = [
            NablaGroup.objects.create(
                name=fake.word()+"-komitéen"
            )
            for _ in range(count)
        ]
        
        count = random.randint(50, 100)
        print("Creating %d NablaUsers" % count)
        for i in range(count):
            username = "komponent%d" % i
            groups = [
                random.choice(ngroups),
                random.choice(classes)
            ]
            user = User.objects.create_user(
                username=username,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                address=fake.address(),
                password='password',
                email=username+'@stud.ntnu.no',
                about=fake.text(),
                birthday=fake.date_time_between_dates(
                    datetime_start=None,
                    datetime_end=None,
                    tzinfo=None),
            )
            
            user.groups.add(*groups)
            user.save()

        if delete:
            NewsArticle.objects.all().delete()

        count = random.randint(10, 20)
        print("Creating %d News" % count)
        for i in range(count):
            NewsArticle.objects.create(
                headline=s(),
                body=g(),
                lead_paragraph=g()
            )

        count = random.randint(10, 20)
        print("Creating %d Events" % count)
        for i in range(count):
            start = fake.date_time_between_dates(
                datetime_start=dt.now(),
                datetime_end=(dt.now()+td(30))
            )

            Event.objects.create(
                headline=s(),
                body=g(),
                lead_paragraph=g(),
                short_name=s(),
                event_start=start,
                event_end=start+td(hours=4),
                organizer=fake.name(),
                location=fake.address()
            )

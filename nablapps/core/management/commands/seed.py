"""
Custom seed script for nablaweb
Currently creates (11.09.2019):
    SuperUser (u: admin, p: admin)
    NablaGroup
    FysmatClass
    NablaUser
    News
    Events
"""
import random
import textwrap
from datetime import datetime as dt
from datetime import timedelta as td

from django.conf import settings
from django.core.management.base import BaseCommand

from faker import Factory

from nablapps.accounts.models import FysmatClass, NablaGroup
from nablapps.accounts.models import NablaUser as User
from nablapps.events.models import Event
from nablapps.news.models import FrontPageNews, NewsArticle

fake = Factory.create("no_NO")  # Norwegian sentences

random.seed()  # Initialize random seed generator


def g():
    """A lot of random text"""
    return fake.text()


def s():
    """Short random string"""
    return textwrap.shorten(fake.sentence(), width=40)


def ss():
    """Longer random string"""
    return textwrap.shorten(fake.sentence(), width=20)


class Command(BaseCommand):
    help = "Puts data into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete", dest="delete", default=True, help="Delete existing data",
        )

    def handle(self, *args, **options):

        if not settings.DEBUG:
            raise Exception("Trying to seed in production.")

        delete = options["delete"]
        print("Deleting old entries: " + str(delete))
        if delete:
            FrontPageNews.objects.all().delete()

        if delete:
            User.objects.all().delete()

        print("Creating superuser admin")
        User.objects.create_user(
            username="admin",
            password="admin",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            email="admin@stud.ntnu.no",
            about=fake.text(),
            birthday=fake.date_time_between_dates(
                datetime_start=None, datetime_end=None, tzinfo=None
            ),
            is_superuser=True,
            is_staff=True,
        )

        if delete:
            NablaGroup.objects.all().delete()

        count = random.randint(5, 10)
        print("Creating %d NablaGroups" % count)
        ngroups = [
            NablaGroup.objects.create(name=fake.word() + "-" + str(i) + "-komitéen")
            for i in range(count)
        ]

        if delete:
            FysmatClass.objects.all().delete()

        count = random.randint(7, 10)
        print("Creating %d FysmatClasses" % count)
        year = dt.now().year
        classes = [
            FysmatClass.objects.create(
                starting_year=year - i, name="kull%d" % (year - i)
            )
            for i in range(count)
        ]

        count = random.randint(50, 100)
        print("Creating %d NablaUsers" % count)
        for i in range(count):
            username = "komponent%d" % i

            user = User.objects.create_user(
                username=username,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                address=fake.address(),
                password="password",
                email=username + "@stud.ntnu.no",
                ntnu_card_number=str(random.randint(int(1e7), int(1e10) - 1)),
                about=fake.text(),
                birthday=fake.date_time_between_dates(
                    datetime_start=None, datetime_end=None, tzinfo=None
                ),
            )

            nabla_group = random.choice(ngroups)
            nabla_group.user_set.add(user)

            fysmat_class = random.choice(classes)
            fysmat_class.user_set.add(user)

        if delete:
            NewsArticle.objects.all().delete()

        count = random.randint(10, 20)
        print("Creating %d News" % count)
        for i in range(count):
            article = NewsArticle.objects.create(
                headline=s(), body=g(), lead_paragraph=g()
            )
            f = FrontPageNews()
            f.content_object = article
            f.save()

        if delete:
            Event.objects.all().delete()

        count = random.randint(10, 20)
        print("Creating %d Events" % count)
        for i in range(count):
            start = fake.date_time_between_dates(
                datetime_start=dt.now() + td(days=2), datetime_end=(dt.now() + td(30))
            )

            event = Event.objects.create(
                headline=s(),
                body=g(),
                lead_paragraph=g(),
                short_name=ss(),
                event_start=start,
                event_end=start + td(hours=4),
                organizer=fake.name(),
                location=fake.address(),
                registration_required=True,
                registration_start=dt.now(),
                registration_deadline=(dt.now() + td(days=2)),
                places=10,
            )
            f = FrontPageNews()
            f.content_object = event
            f.save()

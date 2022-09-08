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
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from faker import Factory

from nablapps.accounts.models import FysmatClass, NablaGroup
from nablapps.accounts.models import NablaUser as User
from nablapps.events.models import Event
from nablapps.interactive.models.code_golf import CodeTask, Result
from nablapps.jobs.models import Advert, Company
from nablapps.news.models import FrontPageNews, NewsArticle

fake = Factory.create("no_NO")  # Norwegian sentences

random.seed()  # Initialize random seed generator


def random_text():
    """A lot of random text"""
    return fake.text()


def random_sentence(maxlen=40):
    """Short random string"""
    return textwrap.shorten(fake.sentence(), width=maxlen)


def _seed_code_golf():
    assert User.objects.exists(), "code golf seed requires at least one user"
    task = CodeTask.objects.create(title="Print j", task="print j", correct_output="j")
    user = User.objects.first()
    Result.objects.create(
        task=task, user=user, solution="print('j') # Prints j", python_version="myVer"
    )
    Result.objects.create(
        task=task, user=user, solution="print('j')", python_version="myVer"
    )
    if User.objects.last() != user:  # Let's have another user submit as well
        Result.objects.create(
            task=task,
            user=User.objects.last(),
            solution="print('j') # Print j",
            python_version="myVer",
        )


class Command(BaseCommand):
    help = "Puts data into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            dest="delete",
            default=True,
            help="Delete existing data",
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
        year = datetime.now().year
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
                headline=random_sentence(),
                body=random_text(),
                lead_paragraph=random_text(),
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
                datetime_start=datetime.now() + timedelta(days=2),
                datetime_end=(datetime.now() + timedelta(days=30)),
            )

            event = Event.objects.create(
                headline=random_sentence(),
                body=random_text(),
                lead_paragraph=random_text(),
                short_name=random_sentence(20),
                event_start=start,
                event_end=start + timedelta(hours=4),
                organizer=fake.name(),
                location=fake.address(),
                registration_required=True,
                registration_start=datetime.now(),
                registration_deadline=(datetime.now() + timedelta(days=2)),
                places=10,
            )
            f = FrontPageNews()
            f.content_object = event
            f.save()

        print("Creating %d Companies and Adverts" % count)
        for i in range(count):
            company = Company.objects.create(
                website="www.example.com",
                name=fake.name(),
                description="company",
            )
            start = fake.date_time_between_dates(
                datetime_start=datetime.now() + timedelta(days=2),
                datetime_end=(datetime.now() + timedelta(days=30)),
            )
            Advert.objects.create(
                company=company,
                headline="stilling_" + str(count),
                removal_date=start + timedelta(days=100),
            )

        print("Creating gode golf challenges")
        _seed_code_golf()

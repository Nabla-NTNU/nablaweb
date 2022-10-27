"""
Seed the database with example data and a superuser (u: admin, pw: admin)

Run the command with --delete to delete seeded data or with
--recreate to delete and re-seed the database

To add new data for seeding create a class that looks like `ObjectSeeder` and
add it to the list in `Command`
"""

import itertools
import random
import textwrap
from datetime import datetime, timedelta
from typing import Protocol

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Factory

from nablapps.accounts.models import FysmatClass, NablaGroup
from nablapps.accounts.models import NablaUser as User
from nablapps.events.models import Event
from nablapps.interactive.models.code_golf import CodeTask, Result
from nablapps.jobs.models import (
    Advert,
    Company,
    RelevantForChoices,
    TagChoices,
    YearChoices,
)
from nablapps.news.models import FrontPageNews, NewsArticle

fake = Factory.create("no_NO")  # Norwegian sentences

random.seed()  # Initialize random seed generator


def random_text():
    """A lot of random text"""
    return fake.text()


def random_sentence(maxlen=40):
    """Short random string"""
    return textwrap.shorten(fake.sentence(), width=maxlen)


class ObjectSeeder(Protocol):
    """Protocol (interface) for seeder functionality"""

    # Descriptions of the objects created/deleted
    description: str
    short_description: str

    @classmethod
    def exists(cls) -> bool:
        """Return True if the objects already exist"""
        ...

    @classmethod
    def create(cls) -> None:
        """Create objects"""
        ...

    @classmethod
    def delete(cls) -> None:
        """
        Delete the objects created by .create()

        NOTE: This should not fail even if no objects exist
        """
        ...


class NablaGroupSeeder:
    amount = 7

    description = f"{amount} NablaGroups"
    short_description = "NablaGroups"

    @classmethod
    def exists(cls) -> bool:
        return NablaGroup.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        for i in range(cls.amount):
            NablaGroup.objects.create(
                name=f"{fake.word()}-{i}-komitéen", group_type="komite"
            )

    @classmethod
    def delete(cls) -> None:
        NablaGroup.objects.all().delete()


class FysmatClassSeeder:
    amount = 10

    description = f"{amount} FysmatClasses"
    short_description = "FysmatClasses"

    @classmethod
    def exists(cls) -> bool:
        return FysmatClass.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        year = datetime.now().year

        for i in range(cls.amount):
            FysmatClass.objects.create(starting_year=year - i, name=f"kull{year - i}")

    @classmethod
    def delete(cls) -> None:
        FysmatClass.objects.all().delete()


class SuperUserSeeder:
    admin_name = "admin"
    admin_password = "admin"

    description = f"superuser '{admin_name}' with password '{admin_password}'"
    short_description = f"superuser '{admin_name}'"

    @classmethod
    def exists(cls) -> bool:
        return User.objects.filter(username=cls.admin_name).exists()

    @classmethod
    def create(cls) -> None:
        committees_qs = NablaGroup.objects.exclude(group_type="kull")
        assert committees_qs.exists(), "Need committees to create users"
        assert FysmatClass.objects.exists(), "Need classes to create users"

        committees = tuple(committees_qs)
        classes = tuple(FysmatClass.objects.all())

        admin_user = User.objects.create_user(
            username=cls.admin_name,
            password=cls.admin_password,
            first_name="Admin",
            last_name=fake.last_name(),
            address=fake.address(),
            email="admin@stud.ntnu.no",
            about=random_text(),
            birthday=fake.date_time_between_dates(
                datetime_start=None, datetime_end=None, tzinfo=None
            ),
            is_superuser=True,
            is_staff=True,
        )

        # Join some committees
        for nabla_group in random.sample(committees, 5):
            nabla_group.user_set.add(admin_user)

        # Join a class
        fysmat_class = random.choice(classes)
        fysmat_class.user_set.add(admin_user)

    @classmethod
    def delete(cls) -> None:
        User.objects.filter(username=cls.admin_name).delete()


class UserSeeder:
    amount = 100

    description = f"{amount} NablaUsers"
    short_description = "NablaUsers"

    @classmethod
    def exists(cls) -> bool:
        return User.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        committees_qs = NablaGroup.objects.exclude(group_type="kull")
        assert committees_qs.exists(), "Need committees to create users"
        assert FysmatClass.objects.exists(), "Need classes to create users"

        committees = tuple(committees_qs)
        classes = tuple(FysmatClass.objects.all())

        # Use a transaction to speed up the creation of users
        # Could do a bulk_create, but want to make sure .save() is called on each user
        with transaction.atomic():
            for i in range(cls.amount):
                username = f"komponent{i}"

                user = User.objects.create_user(
                    username=username,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    address=fake.address(),
                    password="password",
                    email=f"{username}@stud.ntnu.no",
                    ntnu_card_number=str(random.randint(int(1e7), int(1e10) - 1)),
                    about=random_text(),
                    birthday=fake.date_time_between_dates(
                        datetime_start=None, datetime_end=None, tzinfo=None
                    ),
                )

                # Join some committees
                for nabla_group in random.sample(committees, random.randint(0, 5)):
                    nabla_group.user_set.add(user)

                # Join a class
                fysmat_class = random.choice(classes)
                fysmat_class.user_set.add(user)

    @classmethod
    def delete(cls) -> None:
        User.objects.all().delete()


class NewsArticleSeeder:
    amount = 20

    description = f"{amount} NewsArticles"
    short_description = "NewsArticles"

    @classmethod
    def exists(cls) -> bool:
        return NewsArticle.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        for i in range(cls.amount):
            NewsArticle.objects.create(
                headline=random_sentence(),
                body=random_text(),
                lead_paragraph=random_text(),
            )

    @classmethod
    def delete(cls) -> None:
        NewsArticle.objects.all().delete()


class EventSeeder:
    amount = 20

    description = f"{amount} Events"
    short_description = "Events"

    @classmethod
    def exists(cls) -> bool:
        return Event.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        for i in range(cls.amount):
            start = fake.date_time_between_dates(
                datetime_start=datetime.now() + timedelta(days=2),
                datetime_end=(datetime.now() + timedelta(days=30)),
            )

            Event.objects.create(
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

    @classmethod
    def delete(cls) -> None:
        Event.objects.all().delete()


class FrontPageNewsSeeder:
    short_description = description = "FrontPageNews"

    @classmethod
    def exists(cls) -> bool:
        return FrontPageNews.objects.exists()

    @classmethod
    def create(cls) -> None:
        assert NewsArticle.objects.exists(), "Need NewsArticles to create FrontPageNews"
        assert Event.objects.exists(), "Need Events to create FrontPageNews"

        for article in NewsArticle.objects.all():
            f = FrontPageNews()
            f.content_object = article
            f.save()

        for event in Event.objects.all():
            f = FrontPageNews()
            f.content_object = event
            f.save()

    @classmethod
    def delete(cls) -> None:
        FrontPageNews.objects.all().delete()


class CompanyAdvertSeeder:
    amount = 10

    description = f"{amount} Companies and Adverts"
    short_description = "Companies and Adverts"

    amt_classes = 5
    study_directions = ("Industriell matematikk", "Teknisk fysikk", "Biofysikk")
    tags = ("sommerjobb", "deltid", "fulltid", "utlandet")

    @classmethod
    def exists(cls) -> bool:
        return (
            Company.objects.count() >= cls.amount
            and Advert.objects.count() >= cls.amount
            and YearChoices.objects.count() >= cls.amt_classes
            and RelevantForChoices.objects.count() >= len(cls.study_directions)
            and TagChoices.objects.count() >= len(cls.tags)
        )

    @classmethod
    def create(cls) -> None:
        # Create 1.-5. class
        for year in range(1, cls.amt_classes + 1):
            YearChoices.objects.get_or_create(year=year)

        # Create study directions
        for direction in cls.study_directions:
            RelevantForChoices.objects.get_or_create(studieretning=direction)

        # Create tags
        for tag in cls.tags:
            TagChoices.objects.get_or_create(tag=tag)

        years = tuple(YearChoices.objects.all())
        directions = tuple(RelevantForChoices.objects.all())
        tags = tuple(TagChoices.objects.all())

        for i in range(cls.amount - 1, -1, -1):
            company = Company.objects.create(
                website="www.example.com",
                name=fake.company(),
                description=fake.catch_phrase(),
            )
            end_date = fake.date_time_between_dates(
                datetime_start=datetime.now() + timedelta(days=-10),
                datetime_end=datetime.now() + timedelta(days=10),
            ) + timedelta(days=(i - 2) * 30)
            advert = Advert.objects.create(
                company=company,
                headline=f"Stilling hos {company.name}",
                lead_paragraph=f"En veldig kul stilling hos {company.name}!!!!",
                body=(
                    f"Har du alltid hatt lyst til å jobbe hos {company.name}? "
                    "Da er dette muligheten for deg!"
                ),
                deadline_date=end_date,
                removal_date=end_date + timedelta(days=120),
                info_website="www.example.com",
            )
            advert.relevant_for_year.set(
                random.sample(years, random.randint(1, cls.amt_classes))
            )
            advert.relevant_for_group.set(
                random.sample(directions, random.randint(1, len(cls.study_directions)))
            )
            advert.tags.set(random.sample(tags, 1))

    @classmethod
    def delete(cls) -> None:
        Advert.objects.all().delete()
        Company.objects.all().delete()
        YearChoices.objects.all().delete()
        RelevantForChoices.objects.all().delete()
        TagChoices.objects.all().delete()


class CodeGolfSeeder:
    amount = 10

    description = f"{amount} CodeTasks and Results"
    short_description = "CodeTasks and Results"

    @classmethod
    def exists(cls) -> bool:
        return (
            CodeTask.objects.count() >= cls.amount
            and Result.objects.count() >= cls.amount
        )

    @classmethod
    def create(cls) -> None:
        assert User.objects.exists(), "Need users to create code golf"

        all_users = User.objects.all()

        for i in range(cls.amount):
            participating_users = random.sample(all_users, random.randint(3, 20))

            goal = random_sentence()

            task = CodeTask.objects.create(
                title=f"Print '{goal}'",
                task="Write a program that prints '{goal}' to stdout",
                correct_output=goal,
            )

            # Loop over each participating user twice
            # This way each user has 2 submissions
            for user in itertools.chain(participating_users, participating_users):
                explanation = random_text()[: random.randint(1, 50)]
                Result.objects.create(
                    task=task,
                    user=user,
                    solution=f"print('{goal}')  # Explanation: {explanation}",
                    python_version="myVer",
                )

    @classmethod
    def delete(cls) -> None:
        Result.objects.all().delete()
        CodeTask.objects.all().delete()


# The list of seeders in the order the objects should be created
# E.g. if a seeder depends on users existing, it should come after UserSeeder
ALL_SEEDERS: tuple[type[ObjectSeeder], ...] = (
    NablaGroupSeeder,
    FysmatClassSeeder,
    SuperUserSeeder,
    UserSeeder,
    NewsArticleSeeder,
    EventSeeder,
    FrontPageNewsSeeder,
    CompanyAdvertSeeder,
)


def perform_seed(
    seeders: tuple[type[ObjectSeeder], ...], *, delete: bool, recreate: bool
) -> None:
    assert not (delete and recreate), "Cannot delete and recreate at the same time!"

    if delete or recreate:
        print("Deleting old data")
        for seeder in reversed(seeders):
            print(f"\tDeleting {seeder.short_description}")
            seeder.delete()

    if not delete:
        print("Creating new data")
        for seeder in seeders:
            if seeder.exists():
                print(
                    f"\t{seeder.short_description} already exists: skipping... "
                    "Use `seed --recreate` to recreate"
                )
            else:
                print(f"\tCreating {seeder.description}")
                seeder.create()


class Command(BaseCommand):
    help = "Populate the database with example data"

    seeders = ALL_SEEDERS

    def add_arguments(self, parser):
        """Add arguments to the argparser for the command"""
        # Make sure we can't pass --delete and --recreate
        parser.add_mutually_exclusive_group()

        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete existing data",
        )

        parser.add_argument(
            "--recreate",
            action="store_true",
            help="Recreate seeded data",
        )

    def handle(self, *args, **options):
        """Handle the command and do the seeding"""
        if not settings.DEBUG:
            raise Exception("Trying to seed in production.")

        perform_seed(
            ALL_SEEDERS, delete=options["delete"], recreate=options["recreate"]
        )

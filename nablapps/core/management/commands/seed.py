"""
Seed the database with example data and a superuser (u: admin, pw: admin)

Run the command with --delete to delete seeded data or with
--recreate to delete and re-seed the database

To add new data for seeding create a class that looks like `ObjectSeeder` and
add it to the list in `Command`
"""

import functools
import itertools
import random
import textwrap
from datetime import datetime, timedelta
from typing import Protocol

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Factory

from nablapps.accounts.models import FysmatClass, NablaGroup
from nablapps.accounts.models import NablaUser as User
from nablapps.album.models import Album, AlbumForm, AlbumImage
from nablapps.events.models import Event
from nablapps.interactive.models.code_golf import CodeTask, Result
from nablapps.interactive.models.games import Game
from nablapps.jobs.models import (
    Advert,
    Company,
    RelevantForChoices,
    TagChoices,
    YearChoices,
)
from nablapps.nabladet.models import Nablad
from nablapps.news.models import FrontPageNews, NewsArticle
from nablapps.officeCalendar.models import OfficeEvent
from nablapps.podcast.models import Podcast, Season
from nablapps.poll.models import Choice, Poll

fake = Factory.create("no_NO")  # Norwegian sentences

random.seed()  # Initialize random seed generator


def random_text():
    """A lot of random text"""
    return fake.text()


def random_sentence(maxlen=40):
    """Short random string"""
    return textwrap.shorten(fake.sentence(), width=maxlen)


def polygon_picture(size=(256, 256), image_format="png"):
    """
    Return a django file picture with a random polygon

    Generated pictures are stored to disk in var/media/uploads/news_pictures
    """
    return ContentFile(
        fake.image(size=size, image_format=image_format),
        name=f"seed_polygon.{image_format}",
    )


class SeederError(Exception):
    def __init__(self, how_to_fix: str) -> None:
        super().__init__(how_to_fix)
        self.how_to_fix = how_to_fix


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
            about=f"Om meg: {random_text()}",
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

        # Could do a bulk_create, but want to make sure .save() is called on each user
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
                about=f"Om meg: {random_text()}",
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
        assert User.objects.exists(), "Need users to create news article"

        all_users = tuple(User.objects.all())

        for i in range(cls.amount):
            created_date = fake.date_time_between_dates(
                datetime_start=datetime.now() - timedelta(days=30),
            )

            user = random.choice(all_users)

            article = NewsArticle.objects.create(
                headline=f"Nyhet: {random_sentence()}",
                body=f"Innhold: {random_text()}",
                lead_paragraph=f"Første avsnitt: {random_text()}",
                picture=polygon_picture(),
                created_by=user,
                last_changed_by=user,
            )

            article.created_date = created_date
            article.save()

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
        assert Company.objects.exists(), "Need Company to create bedpres Event"
        companies = tuple(Company.objects.all())

        for i in range(cls.amount):
            start = fake.date_time_between_dates(
                datetime_start=datetime.now() + timedelta(days=2),
                datetime_end=(datetime.now() + timedelta(days=30)),
            )

            bedpres = i % 2 == 0

            if bedpres:
                company = random.choice(companies)
                Event.objects.create(
                    headline=f"Bedpres med {company.name}",
                    is_bedpres=True,
                    company=company,
                    body=f"Innhold: {random_text()}",
                    lead_paragraph=f"Første avsnitt: {random_text()}",
                    short_name=f"Bedpres: {random_sentence(15)}",
                    event_start=start,
                    event_end=start + timedelta(hours=4),
                    organizer=fake.name(),
                    location=fake.address(),
                    registration_required=True,
                    registration_start=datetime.now(),
                    registration_deadline=(datetime.now() + timedelta(days=2)),
                    places=random.randint(10, 50),
                    picture=polygon_picture(),
                )
            else:
                Event.objects.create(
                    headline=f"Arrangement: {random_sentence()}",
                    body=f"Innhold: {random_text()}",
                    lead_paragraph=f"Første avsnitt: {random_text()}",
                    short_name=f"Arrangement: {random_sentence(15)}",
                    event_start=start,
                    event_end=start + timedelta(hours=4),
                    organizer=fake.name(),
                    location=fake.address(),
                    registration_required=True,
                    registration_start=datetime.now(),
                    registration_deadline=(datetime.now() + timedelta(days=2)),
                    places=random.randint(10, 100),
                    picture=polygon_picture(),
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
        assert User.objects.exists(), "Need users to create Adverts"

        all_users = tuple(User.objects.all())

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
            user = random.choice(all_users)

            company = Company.objects.create(
                website="https://example.com",
                name=fake.company(),
                description=fake.catch_phrase(),
                picture=polygon_picture(),
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
                info_website="https://example.com",
                created_by=user,
                last_changed_by=user,
            )
            advert.relevant_for_year.set(
                random.sample(years, random.randint(1, cls.amt_classes))
            )
            advert.relevant_for_group.set(
                random.sample(directions, random.randint(1, len(cls.study_directions)))
            )
            advert.tags.set(random.sample(tags, 1))

            advert.created_date = end_date - timedelta(days=30)
            advert.save()

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

        all_users = tuple(User.objects.all())

        for i in range(cls.amount):
            participating_users = random.sample(all_users, random.randint(3, 20))

            goal = random_sentence()

            task = CodeTask.objects.create(
                title=f"Print '{goal}'",
                task=f"Write a program that prints '{goal}' to stdout",
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


class OfficeEventSeeder:
    amount = 7

    description = f"{amount} OfficeEvents"
    short_description = "OfficeEvents"

    @classmethod
    def exists(cls) -> bool:
        return OfficeEvent.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        assert User.objects.exists(), "Need users to create office events"

        all_users = tuple(User.objects.all())

        for i in range(cls.amount):
            start = fake.date_time_between_dates(
                datetime_start=datetime.now(),
                datetime_end=(datetime.now() + timedelta(days=7)),
            )
            contact_person = random.choice(all_users)

            OfficeEvent.objects.create(
                start_time=start,
                end_time=start + timedelta(seconds=30 * 60 * random.randint(1, 8)),
                repeating=True,
                contact_person=contact_person,
                public=i % 2,
                title=f"Kontortid med {contact_person.first_name}",
                description="Det blir kaffe og vafler!",
            )

    @classmethod
    def delete(cls) -> None:
        OfficeEvent.objects.all().delete()


class PollSeeder:
    amount = 5
    amt_votes = 50

    description = f"{amount} Polls with {amt_votes} votes"
    short_description = "Polls and votes"

    @classmethod
    def exists(cls) -> bool:
        return Poll.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        assert User.objects.exists(), "Need users to create polls"

        all_users = tuple(User.objects.all())

        for _ in range(cls.amount):
            user = random.choice(all_users)

            poll = Poll.objects.create(
                question="Hva er ditt favorittall?",
                publication_date=datetime.now(),
                created_by=user,
            )
            choices = []
            for number in range(5):
                choice = Choice.objects.create(
                    poll=poll, choice=str(number), created_by=user
                )
                choices.append(choice)

            for _, user in zip(range(cls.amt_votes), all_users):
                choice = random.choice(choices)
                choice.vote(user)

    @classmethod
    def delete(cls) -> None:
        Poll.objects.all().delete()
        Choice.objects.all().delete()


class PodcastSeeder:
    season_count = 3
    amount_per_season = 5
    total = season_count * amount_per_season

    description = f"{total} Podcasts and {season_count} Seasons"
    short_description = "Podcasts and Seasons"

    @classmethod
    def exists(cls) -> bool:
        return (
            Podcast.objects.count() >= cls.total
            and Season.objects.count() >= cls.season_count
        )

    @classmethod
    def create(cls) -> None:
        for i in range(cls.season_count):
            season, created = Season.objects.get_or_create(
                number=i,
                defaults={
                    # Pass the function to only generate image when needed
                    "logo": polygon_picture,
                    "banner": functools.partial(polygon_picture, size=(1024, 256)),
                },
            )

            for _ in range(cls.amount_per_season):
                name = fake.first_name()

                # TODO: Add an audio file
                Podcast.objects.create(
                    image=polygon_picture(),
                    title=f"En kul podcast med {name}",
                    short_title=f"Podcast med {name}",
                    description="Vi har en veldig interessant samtale med vår gjest",
                    season=season,
                    pub_date=datetime.now(),
                )

    @classmethod
    def delete(cls) -> None:
        Podcast.objects.all().delete()
        Season.objects.all().delete()


class NabladSeeder:
    amount = 10

    description = f"{amount} Nablad"
    short_description = "Nablad"

    @classmethod
    def exists(cls) -> bool:
        return Nablad.objects.count() >= cls.amount

    @classmethod
    def create(cls) -> None:
        now = datetime.now()
        assert User.objects.exists(), "Need users to create nablad"

        all_users = tuple(User.objects.all())

        try:
            for i in range(cls.amount):
                created_date = fake.date_time_between_dates(
                    datetime_start=datetime.now() - timedelta(days=30),
                )

                user = random.choice(all_users)

                nablad = Nablad(
                    pub_date=now + timedelta(days=30 * (i - 5)),
                    file=polygon_picture(size=(500, 1000), image_format="pdf"),
                    is_public=i % 2,
                    headline=f"Nabladet: {random_sentence()}",
                    body=f"Innhold: {random_text()}",
                    lead_paragraph=f"Første avsnitt: {random_text()}",
                    picture=polygon_picture(size=(512, 256)),
                    created_by=user,
                    last_changed_by=user,
                )

                # The save method is weird, so we do this to prevent it from crashing
                nablad.save()

                nablad.created_date = created_date
                nablad.save()
        except Exception as e:
            raise SeederError(how_to_fix="Install ImageMagick to create Nablad") from e

    @classmethod
    def delete(cls) -> None:
        Nablad.objects.all().delete()


class AlbumSeeder:
    amount_albums = 10
    amount_child_albums = 3
    amount_images_per_album = 5

    description = f"{amount_albums} Albums with {amount_child_albums} child Albums. {amount_images_per_album} images per album."
    short_description = "Albums"

    @classmethod
    def exists(cls) -> bool:
        return Album.objects.exists()

    @classmethod
    def create(cls) -> None:
        for i in range(cls.amount_albums):
            parent_album = Album.objects.create(
                title=f"Parent Album: {i+1}", visibility="p" if i % 2 else "u"
            )

            sub_albums = [
                Album.objects.create(
                    title=f"Child Album: {j+1}",
                    visibility="p" if j % 2 else "u",
                    parent=parent_album,
                )
                for j in range(cls.amount_child_albums)
            ]

            all_albums = [parent_album] + sub_albums

            for album in all_albums:
                # Create form
                form = AlbumForm()

                # "upload" the images
                form.files.setlist(
                    "photos",
                    [
                        UploadedFile(file=polygon_picture())
                        for i in range(cls.amount_images_per_album)
                    ],
                )

                form.save_photos(album)

                # Add numbering and description to each image
                images = AlbumImage.objects.filter(album=album)
                for j, img in enumerate(images):
                    img.num = j
                    img.description = random_text()
                    img.save()

    @classmethod
    def delete(cls) -> None:
        Album.objects.all().delete()
        AlbumImage.objects.all().delete()


class GameSeeder:
    description = short_description = "Games"

    @classmethod
    def exists(cls) -> bool:
        return Game.objects.exists()

    @classmethod
    def create(cls) -> None:
        Game.objects.create(
            index=10,
            title="Kodegolf",
            url="kodegolf/",
            picture=polygon_picture(size=(256, 128)),
        )
        Game.objects.create(
            index=10,
            title="NablaPlace",
            url="place/",
            picture=polygon_picture(size=(256, 128)),
        )

    @classmethod
    def delete(cls) -> None:
        Game.objects.all().delete()


# The list of seeders in the order the objects should be created
# E.g. if a seeder depends on users existing, it should come after UserSeeder
ALL_SEEDERS: tuple[type[ObjectSeeder], ...] = (
    NablaGroupSeeder,
    FysmatClassSeeder,
    SuperUserSeeder,
    UserSeeder,
    CompanyAdvertSeeder,
    NewsArticleSeeder,
    EventSeeder,
    FrontPageNewsSeeder,
    CodeGolfSeeder,
    OfficeEventSeeder,
    PollSeeder,
    PodcastSeeder,
    NabladSeeder,
    GameSeeder,
    AlbumSeeder,
)


def perform_seed(
    seeders: tuple[type[ObjectSeeder], ...], *, delete: bool, create: bool
) -> None:
    assert delete or create, "No operation provided"

    if delete:
        print("Deleting old data")
        for seeder in reversed(seeders):
            print(f"\tDeleting {seeder.short_description}")
            seeder.delete()

    if create:
        print("Creating new data")
        for seeder in seeders:
            if seeder.exists():
                print(f"\t{seeder.short_description} already exists: skipping... ")
            else:
                print(f"\tCreating {seeder.description}")
                # Do the creation in a transaction to speed it up
                try:
                    with transaction.atomic():
                        seeder.create()
                except SeederError as e:
                    print(f"\t\tSeeder for {seeder.short_description} failed:")
                    print(f"\t\tFix: {e.how_to_fix}")


class Command(BaseCommand):
    help = "Populate the database with example data"

    seeders = ALL_SEEDERS

    def add_arguments(self, parser):
        """Add arguments to the argparser for the command"""
        # Make sure we can't pass --delete and --preserve
        parser.add_mutually_exclusive_group()

        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete existing data",
        )

        parser.add_argument(
            "--preserve",
            action="store_true",
            help="Preserve existing data",
        )

    def handle(self, *args, delete: bool, preserve: bool, **options):
        """Handle the command and do the seeding"""
        if not settings.DEBUG:
            raise Exception("Trying to seed in production.")

        assert not (delete and preserve), "Cannot both delete and preserve"

        # We recreate (delete+create) by default
        # delete only with --delete
        # create only with --preserve
        perform_delete = not preserve
        perform_create = not delete

        perform_seed(ALL_SEEDERS, delete=perform_delete, create=perform_create)

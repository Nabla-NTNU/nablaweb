# Custom seed script for nablaweb
from accounts.models import NablaUser as User
from content.models.news import News
from content.models.events import Event
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from faker import Factory

fake = Factory.create('no_NO')


def g():
    return fake.text()

    
def s():
    return fake.sentence()


class Command(BaseCommand):
        help = 'Puts data into the database'

        def handle(self, *args, **options):
            
            if not settings.DEBUG:
                raise Exception("Trying to seed in production.")
            
            User.objects.all().delete()
            admin = User.objects.create_user(
                    username='admin',
                    password='admin',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    address=fake.address(),
                    email='admin@stud.ntnu.no',
                    about=fake.text(),
                    birthday=fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None),
                    )
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            
            for i in range(100):
                username = "komponent%d" % (i)
                User.objects.create_user(
                        username=username,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        address=fake.address(),
                        password='password',
                        email=username+'@stud.ntnu.no',
                        about=fake.text(),
                        birthday=fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
                )

            News.objects.all().delete()

            for i in range(0, 10):
                News.objects.create(
                        headline=s(),
                        body=g(),
                        lead_paragraph=g()
                        )


            for i in range(10):
                Event.objects.create(
                    headline=s(),
                    body=g(),
                    lead_paragraph=g(),
                    short_name=g()
                )





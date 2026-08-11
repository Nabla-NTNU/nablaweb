from datetime import date, datetime
from hashlib import sha1

from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.core.mail import send_mail
from django.db import models
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from image_cropping.fields import ImageCropField, ImageRatioField


class NablaUserManager(UserManager):
    def filter_has_birthday_today(self, today=None):
        today = today or date.today()
        return self.filter(
            birthday__day=today.day, birthday__month=today.month, is_active=True
        )

    def get_from_rfid(self, rfid):
        # Assumes only one result
        return self.filter(ntnu_card_number=self.rfid_to_em(rfid)).first()

    @staticmethod
    def rfid_to_em(rfid):
        # Converts number from RFID on NTNU card to EM number written on card.
        # Also works the other way

        # Convert to binary and strip the prefix "0b"
        binary = bin(int(rfid))[2:]

        # Pad with zeros, so it is divisable by 8
        binary = "0" * (8 - len(binary) % 8) + binary

        # Split into 8 bit chuncks
        chunked = [binary[i : i + 8] for i in range(0, len(binary), 8)]

        # Reverse each chuk
        reversed = "".join([chunk[::-1] for chunk in chunked])

        # Convert back to decimal
        decimal = str(int(reversed, 2))

        # Pad with zeros, so it is 10 long
        decimal = decimal.zfill(10)

        return decimal


class NablaUser(AbstractUser):
    telephone = models.CharField(verbose_name="Telefon", max_length=15, blank=True)
    cell_phone = models.CharField(verbose_name="Mobil", max_length=15, blank=True)
    birthday = models.DateField(verbose_name="Bursdag", blank=True, null=True)
    address = models.CharField(verbose_name="Adresse", max_length=40, blank=True)
    mail_number = models.CharField(verbose_name="Postnr", max_length=4, blank=True)
    web_page = models.CharField(verbose_name="Hjemmeside", max_length=80, blank=True)
    wants_email = models.BooleanField(verbose_name="Motta kullmail", default=True)
    about = models.TextField(verbose_name="Biografi", blank=True)
    avatar = ImageCropField(
        verbose_name="Avatar", blank=True, null=True, upload_to="avatars"
    )
    cropping = ImageRatioField(
        # assosiated ImageField:
        "avatar",
        # Ratio and Minimum size
        # (width, height):
        "140x170",
        allow_fullsize=True,
        verbose_name="Beskjæring",
        size_warning=True,
    )
    ntnu_card_number = models.CharField(
        verbose_name="NTNU kortnr",
        max_length=10,
        blank=True,
        help_text=(
            "Dette er et 7-10-sifret nummer på baksiden av kortet. "
            "På nye kort er dette sifrene etter EM. "
            "På gamle kort er dette sifrene nede til venstre. "
            "Det kan brukes of å identifisere deg på bedriftspresentasjoner og andre arrangementer. "
        ),
    )
    darkmode = models.BooleanField(verbose_name="darkmode", default=False)

    objects = NablaUserManager()

    def get_class_number(self):
        """Henter hvilken klasse på fysmat (1-5) brukeren går i.

        Returnerer 0 hvis brukeren ikke går på fysmat."""
        try:
            theclass = FysmatClass.objects.filter(user=self).order_by("starting_year")[
                0
            ]
            return theclass.get_class_number()
        except (FysmatClass.DoesNotExist, IndexError):
            return 0

    def get_absolute_url(self):
        return reverse("member_profile", kwargs={"username": self.username})

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.last_login:
            self.last_login = datetime.today()

        return super().save(force_insert, force_update, using, update_fields)

    def activate(self):
        self.email = f"{self.username}@stud.ntnu.no"
        user_manager = UserManager()
        password = user_manager.make_random_password()
        self.set_password(password)
        self.is_active = True
        self.save()

        template = loader.get_template("accounts/registration_email.txt")
        email_text = template.render({"username": self.username, "password": password})
        self.email_user("Bruker på nabla.no", email_text)

        components_group, _ = NablaGroup.objects.get_or_create(name="komponenter")
        components_group.user_set.add(self)

        fysmat_class = FysmatClass.objects.filter(user=self)
        if fysmat_class.exists():
            send_mail(
                subject="Mail-lsite",
                message=f"Bruker {self.email} har blitt med i kull {fysmat_class[0]}",
                from_email="noreply@nabla.no",
                recipient_list=["webkom@nabla.no"],
                # fail_silently=False,
            )

    @property
    def nablagroups(self):
        groups = self.groups.all()
        return [NablaGroup.objects.filter(id=group.id).first() for group in groups]

    def get_penalties(self):
        """Returns the EventRegistrations for which the user has penalties this semester"""
        from nablapps.events.models import (  # Moved down to avoid loop error when FysmatClass was imported to mixins in events
            EventRegistration,
        )

        # Penalties are valid for six months
        six_months_ago = timezone.now() - timezone.timedelta(
            days=182
        )  # about six months

        penalties = (
            EventRegistration.objects.filter(user=self, date__gte=six_months_ago)
            .exclude(penalty=0)
            .exclude(penalty=None)
        )
        return penalties


class NablaGroup(Group):
    """
    Subklasse av Group som definerer ekstrainformasjon om grupper
    """

    description = models.TextField(verbose_name="Beskrivelse", blank=True)
    mail_list = models.EmailField(verbose_name="Epostliste", blank=True)

    logo = models.FileField(
        upload_to="logos", verbose_name="Logo", blank=True, null=True
    )

    GROUP_TYPES = (
        ("komite", "Komité"),
        ("kull", "Kull"),
        ("studprog", "Studieprogram"),
        ("komleder", "Komitéleder"),
        ("styremedlm", "Styremedlem"),
        ("stilling", "Stilling"),
    )

    group_type = models.CharField(max_length=10, blank=True, choices=GROUP_TYPES)


class FysmatClass(NablaGroup):
    """Gruppe for kull"""

    class Meta:
        verbose_name = "Kull"
        verbose_name_plural = "Kull"

    starting_year = models.CharField("År startet", max_length=4, unique=True, null=True)

    def get_class_number(self):
        now = date.today()
        num = now.year - int(self.starting_year) + int(now.month > 6)
        return 5 if num > 5 else num

    def save(self, *args, **kwargs):
        self.group_type = "kull"
        super().save(*args, **kwargs)


class RegistrationRequest(models.Model):
    username = models.CharField(max_length=80, verbose_name="Brkuernavn")

    created = models.DateTimeField(auto_created=True, verbose_name="Opprettet")

    first_name = models.CharField(max_length=80, verbose_name="Fornavn", null=True)

    last_name = models.CharField(max_length=80, verbose_name="Etternavn", null=True)

    def get_newest_class():
        class_list = FysmatClass.objects.order_by("-starting_year")
        if len(class_list) > 0:
            return class_list[0].id
        return

    fysmat_class = models.ForeignKey(
        FysmatClass, on_delete=models.CASCADE, default=get_newest_class
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.today()
        return super().save(*args, **kwargs)

    def approve_request(self):
        user, _ = NablaUser.objects.get_or_create(username=self.username)

        user.first_name = self.first_name
        user.last_name = self.last_name

        user.activate()

        self.fysmat_class.user_set.add(user)
        components_group, _ = NablaGroup.objects.get_or_create(name="komponenter")
        components_group.user_set.add(user)

        identical_resuests = RegistrationRequest.objects.filter(username=self.username)
        for request in identical_resuests:
            request.delete()

    class Meta:
        verbose_name = "Registreringsforespørsel"
        verbose_name_plural = "Registreringsforespørsler"

    def __str__(self):
        return self.username

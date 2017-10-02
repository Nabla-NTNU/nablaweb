from datetime import datetime, date
from django.contrib.auth.models import Group, AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from hashlib import sha1
from .utils import activate_user_and_create_password, send_activation_email


class NablaUserManager(UserManager):
    def filter_has_birthday_today(self, today=None):
        today = today or date.today()
        return self.filter(birthday__day=today.day,
                           birthday__month=today.month,
                           is_active=True)


class NablaUser(AbstractUser):
    telephone = models.CharField(
        verbose_name="Telefon",
        max_length=15,
        blank=True)
    cell_phone = models.CharField(
        verbose_name="Mobil",
        max_length=15,
        blank=True)
    birthday = models.DateField(
        verbose_name="Bursdag",
        blank=True,
        null=True)
    address = models.CharField(
        verbose_name="Adresse",
        max_length=40,
        blank=True)
    mail_number = models.CharField(
        verbose_name="Postnr",
        max_length=4,
        blank=True)
    web_page = models.CharField(
        verbose_name="Hjemmeside",
        max_length=80,
        blank=True)
    wants_email = models.BooleanField(
        verbose_name="Motta kullmail",
        default=True)
    about = models.TextField(
        verbose_name="Biografi",
        blank=True)
    avatar = models.ImageField(
        verbose_name='Avatar',
        blank=True,
        null=True,
        upload_to='avatars')
    ntnu_card_number = models.CharField(
        verbose_name="NTNU kortnr",
        max_length=10,
        blank=True,
        help_text=(
            "Dette er det 7-10 siffer lange nummeret <b>nede til venstre</b> "
            "på baksiden av NTNU-adgangskortet ditt. "
            "Det brukes blant annet for å komme inn på bedpresser.")
        )

    objects = NablaUserManager()

    def get_hashed_ntnu_card_number(self):
        """Returnerer sha1-hashen av ntnu kortnummeret som BPC-trenger."""
        return sha1(self.ntnu_card_number.encode()).hexdigest()

    def get_class_number(self):
        """Henter hvilken klasse på fysmat (1-5) brukeren går i.

         Returnerer 0 hvis brukeren ikke går på fysmat."""
        try:
            theclass = FysmatClass.objects.filter(user=self).order_by('starting_year')[0]
            return theclass.get_class_number()
        except (FysmatClass.DoesNotExist, IndexError):
            return 0

    def get_absolute_url(self):
        return reverse("member_profile", kwargs={"username": self.username})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.last_login:
            self.last_login = datetime.today()

        return super(NablaUser, self).save(force_insert, force_update, using, update_fields)

    @property
    def nablagroups(self):
        groups = self.groups.all()
        return [NablaGroup.objects.filter(id=group.id).first() for group in groups]


class NablaGroup(Group):
    """
    Subklasse av Group som definerer ekstrainformasjon om grupper
    """
    description = models.TextField(verbose_name="Beskrivelse", blank=True)
    mail_list = models.EmailField(verbose_name="Epostliste", blank=True)

    logo = models.FileField(
        upload_to="logos",
        verbose_name="Logo",
        blank=True,
        null=True
    )

    GROUP_TYPES = (
        ('komite', 'Komité'),
        ('kull', 'Kull'),
        ('studprog', 'Studieprogram'),
        ('komleder', 'Komitéleder'),
        ('styremedlm', 'Styremedlem'),
        ('stilling', 'Stilling'),
    )

    group_type = models.CharField(max_length=10, blank=True, choices=GROUP_TYPES)


class FysmatClass(NablaGroup):
    """ Gruppe for kull """

    class Meta:
        verbose_name = "Kull"
        verbose_name_plural = "Kull"

    starting_year = models.CharField("År startet", max_length=4, unique=True)

    def get_class_number(self):
        now = date.today()
        num = now.year - int(self.starting_year) + int(now.month > 6)
        return 5 if num > 5 else num

    def save(self, *args, **kwargs):
        self.group_type = 'kull'
        super().save(*args, **kwargs)


class RegistrationRequest(models.Model):
    username = models.CharField(
        max_length=80,
        verbose_name="Brkuernavn"
    )

    created = models.DateTimeField(
        auto_created=True,
        verbose_name="Opprettet"
    )

    first_name = models.CharField(
        max_length=80,
        verbose_name="Fornavn",
        null=True
    )

    last_name = models.CharField(
        max_length=80,
        verbose_name="Etternavn",
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.today()
        return super(RegistrationRequest, self).save(*args, **kwargs)

    def approve_request(self):
        user, created_user = NablaUser.objects.get_or_create(username=self.username)

        user.first_name = self.first_name
        user.last_name = self.last_name

        password = activate_user_and_create_password(user)
        send_activation_email(user, password)

    class Meta:
        verbose_name = "Registreringsforespørsel"
        verbose_name_plural = "Registreringsforespørsler"

    def __str__(self):
        return self.username

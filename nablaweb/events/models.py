# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.template import loader, Context

from urlparse import urlparse
import datetime
from news.models import News


class RegistrationException(Exception):
    def __init__(self, token):
        self.token = token


class AbstractEvent(News):
    """
    Abstrakt modell som definerer det som er felles
    for Event og BedPres.
    """
    short_name = models.CharField("kort navn", max_length=20, blank=True, null=True,
            help_text="Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.")
    organizer = models.CharField(verbose_name="organisert av", max_length=100, blank=True, help_text="Den som står bak arrangementet")
    location = models.CharField(u"sted", max_length=100, blank=False)
    event_start = models.DateTimeField(verbose_name="start", null=True, blank=False)
    event_end = models.DateTimeField(verbose_name="slutt", null=True, blank=True)
    facebook_url = models.CharField(verbose_name="facebook-url", blank=True, max_length=100,
            help_text="URL-en til det tilsvarende arrangementet på Facebook")

    # Medlemsvariabler som har med påmelding å gjøre. De fleste er kun relevant
    # hvis registration_required er satt til True.
    registration_required = models.BooleanField(verbose_name="påmelding", default=False, null=False, blank=False)
    registration_deadline = models.DateTimeField(verbose_name="påmeldingsfrist", null=True, blank=True)
    registration_start = models.DateTimeField(verbose_name="påmelding åpner", null=True, blank=True)
    deregistration_deadline = models.DateTimeField(verbose_name="avmeldingsfrist", null=True, blank=True)
    places = models.PositiveIntegerField(verbose_name="antall plasser", null=True, blank=True)

    has_queue = models.NullBooleanField(verbose_name="har venteliste", null=True, blank=True,
            help_text="""Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.""")

    open_for = models.ManyToManyField(Group, verbose_name = "Åpen for", blank = True, null = True,
            help_text = "Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.")

    class Meta:
        abstract = True

    def allowed_to_attend(self, user):
        "Indikerer om en bruker har lov til å melde seg på arrangementet"
        return (not self.open_for.exists()) or self.open_for.filter(user=user).exists()

    def has_started(self):
        now = datetime.datetime.now()
        return self.event_start < now

    def has_finished(self):
        now = datetime.datetime.now()
        return self.event_end < now

    def registration_open(self):
        try:
            now = datetime.datetime.now()
            return self.registration_required \
                and (self.registration_start is None or (now > self.registration_start)) \
                and now < self.registration_deadline
        except:
            return False

    def deregistration_closed(self):
        return self.deregistration_deadline and (self.deregistration_deadline < datetime.datetime.now())

    def __unicode__(self):
        return u'%s, %s' % (self.headline, self.event_start.strftime('%d.%m.%y'))

    def get_short_name(self):
        " Henter short_name hvis den finnes, og kutter av enden av headline hvis ikke."
        if self.short_name:
            return self.short_name
        else:
            return self.headline[0:18].capitalize() + '...'


class Event(AbstractEvent):
    """Arrangementer både med og uten påmelding.
    Dukker opp som nyheter på forsiden.
    """

    class Meta:
        verbose_name = "arrangement"
        verbose_name_plural = "arrangement"
        permissions=(
                ("administer", "Can administer events"),
        )

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        self._prune_queue()

    def delete(self, *args, **kwargs):
        self.eventregistration_set.all().delete()
        super(Event, self).delete(*args, **kwargs)

    def clean(self):
        self.clean_facebook_url()

    def clean_facebook_url(self):
        """Verifiserer formen på facebook-urlen, og endrer den hvis den er feil."""
        parsed = urlparse(self.facebook_url)
        noscheme = parsed.netloc + parsed.path
        self.facebook_url = 'http' + '://' + noscheme.replace("http://", "").replace("https://", "")

        if (self.facebook_url == "http://"):
            self.facebook_url = ""

    @property
    def registrations_manager(self):
        return EventRegistration.get_manager_for(self)

    @property
    def waiting_registrations(self):
        return self.registrations_manager.waiting_ordered()

    @property
    def attending_registrations(self):
        return self.registrations_manager.attending_ordered()

    def free_places(self):
        """Returnerer antall ledige plasser.

        dvs antall plasser som umiddelbart gir brukeren en garantert plass, og ikke bare
        ventelisteplass.
        Returnerer 0 hvis self.places er None.
        """
        try:
            return max(self.places - self.users_attending(), 0)
        except TypeError:
            return 0

    def is_full(self):
        return self.free_places() == 0

    def users_attending(self):
        """Returnerer antall brukere som er påmeldt."""
        return self.attending_registrations.count()

    def users_waiting(self):
        """Returnerer antall brukere som står på venteliste."""
        return self.waiting_registrations.count()

    def percent_full(self):
        """Returnerer hvor mange prosent av plassene som er tatt."""
        if self.places == None:
            return 0
        elif  self.places != 0:
            return min(self.users_attending() * 100 / self.places, 100)
        else:
            return 100

    def users_registered(self):
        """Returnerer totalt antall brukere som er registrerte.

        Dvs. både påmeldte og de som står på venteliste."""
        return self.eventregistration_set.count()

    def is_registered(self, user):
        return self.eventregistration_set.filter(user=user).exists()
    def is_attending(self, user):
        return self.attending_registrations.filter(user=user).exists()
    def is_waiting(self, user):
        return self.waiting_registrations.filter(user=user).exists()

    def get_users_registered(self):
        return [e.user for e in self.eventregistration_set.all()]
    def get_users_attending(self):
        return [e.user for e in self.attending_registrations]
    def get_users_waiting(self):
        return [e.user for e in self.waiting_registrations]

    def register_user(self, user, ignore_restrictions=False):
        """Forsøker å melde brukeren på arrangementet.

        Kaster RegistrationException hvis det misslykkes.
        """
        if not self.registration_required:
            raise RegistrationException("noreg")
        elif ignore_restrictions:
            pass
        elif not self.registration_open():
            raise RegistrationException("unopened")
        elif not self.allowed_to_attend(user):
            raise RegistrationException("not_allowed")

        # TODO: Bruk select_for_update(), når den blir tilgjengelig.
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-for-update
        regs = self.eventregistration_set # .select_for_update()
        try:
            reg = regs.get(user=user)
        except EventRegistration.DoesNotExist:
            pass
        else:
            return reg

        if not self.is_full():
            reg = regs.create(event=self, user=user, number=self.users_attending()+1, attending=True)
        elif self.has_queue:
            reg = regs.create(event=self, user=user, number=self.users_waiting()+1, attending=False)
        else:
            raise RegistrationException("full")
        return reg

    def deregister_user(self, user):
        """Melder brukeren av arrangementet.

        I praksis sørger metoden bare for at brukeren ikke er påmeldt lengre, uavhengig av status før.
        """
        regs = self.eventregistration_set
        if self.deregistration_closed():
            raise RegistrationException("dereg_closed")
        try:
            reg = regs.get(user=user)
            self.eventregistration_set.get(user=user).delete()
        except EventRegistration.DoesNotExist:
            raise RegistrationException("not_reg")
        else:
            self.update_lists()

    def update_lists(self):
        self._fix_list_numbering()
        self._move_waiting_to_attending()

    def _fix_list_numbering(self):
        attending_regs = self.attending_registrations
        for n, reg in enumerate(attending_regs, start=1):
            reg.number = n
            reg.save()

        waiting_regs = self.waiting_registrations
        for n, reg in enumerate(waiting_regs, start=1):
            reg.number = n
            reg.save()

    def _move_waiting_to_attending(self):
        if self.registration_open() and not self.has_started():
            while(min(self.free_places(), self.waiting_registrations.count()) > 0):
                reg = self.registrations_manager.first_on_waiting_list()
                reg.set_attending()
            self._fix_list_numbering()

    def _prune_queue(self):
        """Sletter overflødige registreringer."""
        if not self.registration_required:
            self.eventregistration_set.all().delete()
        elif not self.has_queue:
            self.waiting_registrations.delete()


class EventRegistration(models.Model):
    """Modell for påmelding på arrangementer.

    Inneholder både påmeldinger og venteliste.
    For ventelistepåmelding er attending satt til False og førstmann på ventelista har number=1.
    """

    event = models.ForeignKey(Event, blank=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, verbose_name='bruker')
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Påmeldingsdato")

    number = models.PositiveIntegerField(blank=True, null=True, verbose_name='kønummer',
            help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.')

    attending = models.BooleanField(blank=False, null=False, default=True, verbose_name='har plass',
            help_text="Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.")

    def __unicode__(self):
        return u'EventRegistration: %s, %s: %s' % (self.event, self.attending, self.user)

    @classmethod
    def get_manager_for(cls, event):
        """Henter en manager for en gitt event."""
        return RelatedEventRegistrationManager(event)

    def is_waiting_place(self):
        "Returnerer True dersom registreringen er en plass på venteliste."
        return not self.attending

    def waiting_list_place(self):
        "Returnerer hvilken plass man har på ventelisten. None hvis man har plass eller det ikke finnes."
        if not self.attending:
            return self.number
        else:
            return None

    def set_attending(self):
        "Flytter noen fra ventelisten til påmeldte"
        if not self.attending:
            self.attending = True
            self.number = self.event.users_attending() + 1
            self.save()
            if self.user.email:
                subject = u'Påmeldt %s' % self.event.headline
                template = loader.get_template("events/moved_to_attending_email.txt")
                message = template.render(Context({'event': self, 'name': self.user.get_full_name()}))
                self.user.email_user(subject, message)

    def is_attending_place(self):
        "Returnerer True dersom registreringen er en garantert plass."
        return self.attending
    is_attending_place.boolean = True
    is_attending_place.short_description = "har plass"

    class Meta:
        verbose_name = 'påmelding'
        verbose_name_plural = 'påmeldte'


class RelatedEventRegistrationManager(models.Manager):

    def __init__(self, event):
        self.event = event

    def get_queryset(self):
        return EventRegistration.objects.filter(event=self.event)

    def waiting(self):
        return self.get_queryset().filter(attending=False)

    def waiting_ordered(self):
        return self.waiting().order_by('number')

    def attending(self):
        return self.get_queryset().filter(attending=True)

    def attending_ordered(self):
        return self.attending().order_by('number')

    def first_on_waiting_list(self):
        """Hente førstemann på ventelista."""
        return self.waiting_ordered()[0]


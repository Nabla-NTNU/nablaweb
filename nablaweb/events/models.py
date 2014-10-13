# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings

from urlparse import urlparse
import datetime
from news.models import News


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

    def registration_open(self):
        try:
            now = datetime.datetime.now()
            return self.registration_required and (now < self.registration_deadline) and (now > self.registration_start)
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
                ("administer","Can administer events"),
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

    def free_places(self):
        """Returnerer antall ledige plasser.

        dvs antall plasser som umiddelbart gir brukeren en garantert plass, og ikke bare
        ventelisteplass.
        Returnerer 0 hvis self.places er None.
        """
        try:
            return max(self.places - self.eventregistration_set.filter(attending = True).count(), 0)
        except TypeError:
            return 0

    def is_full(self):
        return self.free_places() == 0

    def users_attending(self):
        """Returnerer antall brukere som er påmeldt."""
        return self.eventregistration_set.filter(attending = True).count()

    def users_waiting(self):
        """Returnerer antall brukere som står på venteliste."""
        return self.eventregistration_set.filter(attending = False).count()

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
        return self.eventregistration_set.filter(user=user,attending=True).exists()
    def is_waiting(self, user):
        return self.eventregistration_set.filter(user=user,attending=False).exists()

    def has_waiting_list(self):
        """Returnerer True dersom arrangementet har venteliste, False ellers."""
        return bool(self.has_queue)

    def get_users_registered(self):
        return [e.user for e in self.eventregistration_set.all()]
    def get_users_attending(self):
        return [e.user for e in self.eventregistration_set.filter(attending=True)]
    def get_users_waiting(self):
        return [e.user for e in self.eventregistration_set.filter(attending=False)]

    def register_user(self, user):
        """
        Forsøker å melde brukeren på arrangementet.  Returnerer en
        tekststreng som indikerer hvor vellykket operasjonen var.
        """
        if not self.registration_required:
            msg = 'noreg'
        else:
            # TODO: Bruk select_for_update(), når den blir tilgjengelig.
            # https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-for-update
            regs = self.eventregistration_set # .select_for_update()
            try:
                reg = regs.get(user=user)
                msg = 'reg_exists'
            except EventRegistration.DoesNotExist:
                if self.is_full():
                    if self.has_waiting_list():
                        reg = regs.create(event=self, user=user, number=self.users_waiting()+1, attending=False)
                        msg = 'queue'
                    else:#No waiting list
                        msg = 'full'
                else:
                    reg = regs.create(event=self, user=user, number=self.users_attending()+1, attending=True)
                    msg = 'attend'
        return msg

    def deregister_user(self, user):
        """
        Melder brukeren av arrangementet. I praksis sørger metoden bare
        for at brukeren ikke er påmeldt lengre, uavhengig av status før.
        """
        regs = self.eventregistration_set
        try:
            reg = regs.get(user=user)
            self.eventregistration_set.get(user=user).delete()
            self.update_lists()
            msg = 'dereg'
        # Brukeren er ikke påmeldt
        except EventRegistration.DoesNotExist:
            msg = 'not_reg'
        self.update_lists()
        return msg

    def update_lists(self):
        self._fix_list_numbering()
        self._move_waiting_to_attending()

    def _fix_list_numbering(self):
        attending_regs = self.eventregistration_set.filter(attending=True).order_by("number")
        for n, reg in enumerate(attending_regs, start=1):
            reg.number = n
            reg.save()

        waiting_regs = self.eventregistration_set.filter(attending=False).order_by("number")
        for n, reg in enumerate(waiting_regs, start=1):
            reg.number = n
            reg.save()

    def _move_waiting_to_attending(self):
        if self.registration_deadline and self.registration_deadline > datetime.datetime.now() and datetime.datetime.now() + datetime.timedelta(1) < self.event_start :
            waiting_list = list( self.eventregistration_set.filter(attending=False).order_by('number').reverse() )
            for n in xrange( min(self.free_places(), len(waiting_list)) ):
                waiting_list.pop().set_attending()
            for eventregistration in waiting_list:
                eventregistration.number -= waiting_list[-1].number-1
                eventregistration.save()

    def _prune_queue(self):
        """Sletter overflødige registreringer."""
        # Dersom registrering ikke trengs lengre.
        if not self.registration_required:
            self.eventregistration_set.all().delete()

        # Dersom arrangementet ikke har venteliste lengre.
        elif not self.has_waiting_list():
            self.eventregistration_set.filter(attending = False).delete()


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
                message = u'''Hei %s
                Du har nå fått plass på arrangementet "%s". Plassen er tildelt fordi du stod på venteliste.'''                        %(self.user.get_full_name(), self.event.headline)
                if self.event.deregistration_deadline and self.event.deregistration_deadline < datetime.datetime.now():
                    message += u''' Fristen for å melde seg av arrangementet har gått ut. Husk at du kan få prikk dersom du ikke møter opp. Dersom du allikevel ikke kan komme, kan du prøve å ta kontakt med %s så fort som mulig.'''%(self.event.organizer)
                elif self.event.deregistration_deadline:
                    message += u''' Hvis du allikevel ikke kan komme, må du melde deg av før avmeldingsfristen. Husk at du kan få prikk dersom du ikke møter opp.'''
                else:
                    message += u''' Hvis du ikke kan komme, må du huske å melde deg av så fort som mulig. Husk at du kan få prikk dersom du ikke møter opp.'''

                self.user.email_user(subject, message)

    def is_attending_place(self):
        "Returnerer True dersom registreringen er en garantert plass."
        return self.attending
    is_attending_place.boolean = True
    is_attending_place.short_description = "har plass"

    class Meta:
        verbose_name = 'påmelding'
        verbose_name_plural = 'påmeldte'

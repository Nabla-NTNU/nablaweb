# -*- coding: utf-8 -*-

from django.db import models
from content.models import AbstractEvent
from jobs.models import Company
from accounts.models import NablaUser as User

from . import bpc_core


def get_bpc_user_dictionary(user):
    """Henter brukerinformasjonen BPC krever fra et User objekt."""
    return {"fullname": user.get_full_name(),
            "username": user.username,
            "card_no": user.get_hashed_ntnu_card_number(),
            "year": str(user.get_class_number())}


class BedPres(AbstractEvent):
    """
    Modell som lagrer informasjon om en bedpress fra BPC.
    """

    bpcid = models.CharField(
        verbose_name="BPC-id",
        max_length=16,
        unique=True,
        blank=False,
        help_text=("Dette er id'en som blir brukt internt hos BPC. "
                   "Ikke endre den hvis du ikke vet du gjør."))
    company = models.ForeignKey(
        Company,
        verbose_name="Bedrift",
        blank=False,
        help_text="Hvilken bedrift som står bak bedriftspresentasjonen")

    # Informajon fra BPC som blir lastet ned av metodene
    # bpc_info,bpc_waiting_list og bpc_attending_list ved behov.
    _bpc_info = {}
    _bpc_waiting_list = []
    _bpc_attending_list = []

    class Meta:
        verbose_name = "bedriftspresentasjon"
        verbose_name_plural = "bedriftspresentasjoner"

    def register_user(self, user):
        # TODO feilhåndtering bør ikke skje her, men jeg fikk ikke til å ta i
        # mot BPCResponseException i register_user view - hiasen
        card_no = user.ntnu_card_number
        if not card_no or not card_no.isdigit():
            return "Du ble ikke påmeldt fordi du ikke har registrert gyldig kortnummer."

        user_dict = get_bpc_user_dictionary(user)
        try:
            response = bpc_core.add_attending(event=self.bpcid, **user_dict)
        except bpc_core.BPCResponseException as exception:
            return exception.message  # TODO Bruke noen andre feilmeldinger. Er litt kryptiske for brukere
        if response['add_attending'][0] == '1':
            return "Du ble påmeldt"
        else:
            return "Du står nå på venteliste"

    def deregister_user(self, user):
        try:
            response = bpc_core.rem_attending(event=self.bpcid, username=user.username)
            return "Du ble meldt av"
        except bpc_core.BPCResponseException as exception:
            return exception.message

    def get_attendance_list(self):
        return User.objects.filter(username__in=self.bpc_attending_list)

    def get_waiting_list(self):
        return User.objects.filter(username__in=self.bpc_waiting_list)

    def is_registered(self, user):
        return self.is_attending(user) or self.is_waiting(user)

    def is_waiting(self, user):
        return user.username in self.bpc_waiting_list

    def is_attending(self, user):
        return user.username in self.bpc_attending_list

    def free_places(self):
        return int(self.bpc_info.get('seats_available', 0))

    def is_full(self):
        return self.free_places() == 0

    def users_attending(self):
        return int(self.bpc_info.get('this_attending', 0))

    def users_waiting(self):
        return len(self.bpc_waiting_list)

    def percent_full(self):
        if self.places == None:
            self.places = self.bpc_info.get('seats', 0)
            self.save()
        if self.places != 0:
            return ((self.places - self.free_places()) * 100) / self.places
        else:
            return 100

    def correct_picture(self):
        return self.picture if self.picture else self.company.picture

    def correct_cropping(self):
        return self.cropping if self.picture else self.company.cropping

    def open_for_classes(self):
        bpc_info = self.bpc_info
        min_year = bpc_info['min_year']
        max_year = bpc_info['max_year']
        if max_year == '99':
            max_year = ''
        if min_year == max_year:
            return min_year
        else:
            return min_year + '-' + max_year

    @property
    def bpc_info(self):
        """
        Laster ned informasjon om bedpressen fra BPC og lagrer det midlertidig i
        BedPres-objektet. Brukes som en vanlig variabel, ikke funksjon.
        """
        if not self._bpc_info:
            try:
                self._bpc_info = bpc_core.get_events(event=self.bpcid)['event'][0]
                for x in ['time', 'deadline', 'registration_start']:
                    self._bpc_info[x] = bpc_core.bpc_time_to_datetime(self._bpc_info[x])
                self._bpc_info['seats'] = int(self._bpc_info['seats'])
            except bpc_core.BPCResponseException:
                return {}
        return self._bpc_info

    @property
    def bpc_attending_list(self):
        if not self._bpc_attending_list:
            try:
                self._bpc_attending_list = [x['username'] for x in bpc_core.get_attending(event=self.bpcid)['users']]
            except bpc_core.BPCResponseException:
                return []
        return self._bpc_attending_list

    @property
    def bpc_waiting_list(self):
        if not self._bpc_waiting_list:
            try:
                self._bpc_waiting_list = [x['username'] for x in bpc_core.get_waiting(event=self.bpcid)['users']]
            except bpc_core.BPCResponseException:
                return []
        return self._bpc_waiting_list

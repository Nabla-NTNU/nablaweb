# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from events.models import AbstractEvent
from hashlib import sha1
from news.models import News
import bpc_core


class BedPres(AbstractEvent):
    bpcid = models.CharField(verbose_name="BPC-id", max_length=16, unique=True, blank=True, help_text = "Dette er id'en som blir brukt internt hos BPC. Ikke endre den hvis du ikke vet du gjør.")
    _bpc_info = []
    _bpc_waiting_list = []
    _bpc_attending_list = []

    class Meta:
        verbose_name = "bedriftspresentasjon"
        verbose_name_plural = "bedriftspresentasjoner"

    def register_user(self, user):
        # TODO feilhåndtering bør ikke skje her, men jeg fikk ikke til å ta i
        # mot BPCResponseException i register_user view - hiasen
        try:
            response = bpc_core.add_attending(
                fullname=user.get_full_name(),
                username=user.username,
                card_no=sha1(user.get_profile().ntnu_card_number).hexdigest(),
                event=self.bpcid,
                year='1', # FIXME
                )
        except bpc_core.BPCResponseException as exception:
            return exception.message # TODO Bruke noen andre feilmeldinger. Er litt kryptiske for brukere
        return "Du ble påmeldt"

    def deregister_user(self, user):
        try:
            response = bpc_core.rem_attending(event=self.bpcid, username=user.username)
            return "Du ble meldt av"
        except bpc_core.BPCResponseException as exception:
            return exception.message 

    def is_registered(self, user):
        return user.username in self.bpc_attending_list

    def is_waiting(self,user):
        return user.username in self.bpc_waiting_list

    def free_places(self):
        return int(self.bpc_info['seats_available'])

    def is_full(self):
        return free_places() == 0


    # Laster ned informasjon om bedpressen fra BPC og lagrer det midlertidig i
    # BedPres-objektet. Kan brukes som en vanlig variabel.
    @property
    def bpc_info(self):
        if not self._bpc_info:
            try: 
                self._bpc_info = bpc_core.get_events(event=self.bpcid)['event'][0]
            except bpc_core.BPCResponseError:
                pass
        return self._bpc_info

    
    @property
    def bpc_attending_list(self):
        if not self._bpc_attending_list:
            try: 
                self._bpc_attending_list = [x['username'] for x in bpc_core.get_attending(event=self.bpcid)['users']]
            except bpc_core.BPCResponseError:
                pass
        return self._bpc_attending_list
    @property
    def bpc_waiting_list(self):
        if not self._bpc_waiting_list:
            try: 
                self._bpc_waiting_list =[x['username'] for x in bpc_core.get_waiting(event=self.bpcid)['users']]
            except bpc_core.BPCResponseError:
                return []
        return self._bpc_waiting_list

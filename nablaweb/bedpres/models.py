# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from hashlib import sha1
import bpc_core

class BedPres(Event):
    bpcid = models.CharField(verbose_name="BPC-id", max_length=16, unique=True, blank=True)

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
        return NotImplemented
        response = bpc_core.rem_attending(
            event=self.bpc_id,
            username=user.username,
            )

    def is_registered(self, user):
        try:
            response = bpc_core.get_attending(event = self.bpcid)
            usernames = [u['username'] for u in response['users']]
            return user.username in usernames
        except bpc_core.BPCResponseException:
            return False 



    def move_user_to_place(self, user, place):
        return NotImplemented

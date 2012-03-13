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
        return NotImplemented
        response = bpc_core.add_attending(
            fullname=user.get_full_name(),
            username=user.username,
            card_no=sha1(user.ntnu_card_number).hexdigest(),
            event=self.bpc_id,
            year='1', # FIXME
            )

    def deregister_user(self, user):
        return NotImplemented
        response = bpc_core.rem_attending(
            event=self.bpc_id,
            username=user.username,
            )

    def move_user_to_place(self, user, place):
        return NotImplemented

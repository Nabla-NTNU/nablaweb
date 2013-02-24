# -*- coding: utf-8 -*-

from datetime import datetime
from itertools import chain

from django.db import models
from django.contrib.auth.models import User
from events.models import AbstractEvent
from jobs.models import Company
from hashlib import sha1
from news.models import News
import bpc_core


class BedPres(AbstractEvent):
    """
    Modell som lagrer informasjon om en bedpress fra BPC.
    """

    # Id'en til bedpressen internt hos BPC
    bpcid = models.CharField(verbose_name="BPC-id", max_length=16, unique=True, blank=True, help_text = "Dette er id'en som blir brukt internt hos BPC. Ikke endre den hvis du ikke vet du gjør.")
    company = models.ForeignKey(Company, verbose_name="Bedrift", blank=False, help_text="Hvilken bedrift som står bak bedriftspresentasjonen")

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
        card_no = user.get_profile().ntnu_card_number
        if not card_no or not card_no.isdigit():
            return "Du ble ikke påmeldt fordi du ikke har registrert gyldig kortnummer."

        try:
            response = bpc_core.add_attending(
                fullname=user.get_full_name(),
                username=user.username,
                card_no=sha1(user.get_profile().ntnu_card_number).hexdigest(),
                event=self.bpcid,
                year=str(user.get_profile().get_class_number()), # FIXME
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

    def get_users_registered(self):
        return chain(self.get_users_attending(),self.get_users_waiting())

    def get_users_attending(self):
        return User.objects.filter(username__in=self.bpc_attending_list)

    def get_users_waiting(self):
        return User.objects.filter(username__in=self.bpc_waiting_list)
        
    def is_registered(self, user):
        return self.is_attending(user) or self.is_waiting(user)

    def is_waiting(self,user):
        return user.username in self.bpc_waiting_list

    def is_attending(self,user):
        return user.username in self.bpc_attending_list

    def free_places(self):
        return int(self.bpc_info.get('seats_available',0))

    def is_full(self):
        return free_places() == 0

    def users_attending(self):
        return int(self.bpc_info.get('this_attending',0))

    def users_waiting(self):
        return User.objects.filter(username__in=self.bpc_waiting_list)
    
    def users_registered(self):
        return list(self.users_attending())+list(self.users_waiting())

    def percent_full(self):
        if self.places == None:
            self.places = self.bpc_info.get('seats',0)
            self.save()
        if self.places !=0:
            return ((self.places - self.free_places())*100)/self.places
        else:
            return 100

    def correct_picture(self): return self.company.picture
    def correct_cropping(self): return self.company.cropping

    @property
    def bpc_info(self):
        """
        Laster ned informasjon om bedpressen fra BPC og lagrer det midlertidig i
        BedPres-objektet. Brukes som en vanlig variabel, ikke funksjon.
        """
        if not self._bpc_info:
            try:
                self._bpc_info = bpc_core.get_events(event=self.bpcid)['event'][0]
                for x in ['time','deadline','registration_start']:
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
                self._bpc_waiting_list =[x['username'] for x in bpc_core.get_waiting(event=self.bpcid)['users']]
            except bpc_core.BPCResponseException:
                return []
        return self._bpc_waiting_list

    def update_info_from_bpc(self):
        """
        Oppdaterer informasjon fra BPC
        """
        bpc_info = self.bpc_info
        self.headline = bpc_info['title']
        self.slug = bpc_info['title'].strip().replace(' ','-')
#       picture = bpc_info['logo']

        from django.core.files import File
        import urllib
        import os

        #if not self.picture:
       # result = urllib.urlretrieve(self.bpc_info['logo']) # image_url is a URL to an image
       # filename,file_ext = os.path.splittext(self.bpc_info['logo'])

        #self.picture.save(
         #   os.path.basename("news_pictures/bpc_"+self.bpcid+file_ext ),
          #  File(open(result[0]))
           # )
        #self.save()
            
        self.body = bpc_info['description']
        self.organizer = 'Bedkom'
        self.location = bpc_info['place']
        self.event_start = bpc_info['time']
        self.registration_required = True
        self.registration_start = bpc_info['registration_start']
        self.registration_deadline = bpc_info['deadline']
        self.places = bpc_info['seats']
        self.has_queue = bool(bpc_info['waitlist_enabled'])

        self.save()
 

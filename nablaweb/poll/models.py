# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class Poll(models.Model):
    question = models.CharField('Spørsmål', max_length=1000)
    creation_date = models.DateTimeField('Opprettet', auto_now_add=True)
    publication_date = models.DateTimeField('Publisert')
    added_by = models.CharField('Lagt til av', max_length=100)
    edit_date = models.DateTimeField('Sist endret', auto_now=True)
    is_current = models.BooleanField('Nåværende avstemning?')
    users_voted = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Brukere som har stemt', editable=False)
    users_voted.help_text = '' # For å fjerne infomeldingen om hvordan man velger brukere (noe som ikke er mulig) i admin
    
    def __unicode__(self):
        return self.question
        
    def save(self, *args, **kwargs):
        current_poll = Poll.objects.filter(is_current=True)
        if (current_poll and self.is_current):
            current_poll[0].is_current = False
            current_poll[0].save()
        super(Poll, self).save(*args, **kwargs)
        
    def get_total_votes(self):
        sum = 0
        for i in self.choice_set.all():
            sum += i.votes
        return sum

    def user_has_voted(self, user):
        return user in self.users_voted.all()
        
    class Meta:
        verbose_name = "avstemning"
        verbose_name_plural = "avstemninger"
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField('Navn på valg', max_length=80)
    votes = models.IntegerField('Antall stemmer', blank=False, default=0)
    creation_date = models.DateTimeField('Lagt til', auto_now_add=True)
    added_by = models.CharField('Lagt til av', max_length=100) # Hvem som la til valget i avstemningen
    
    def __unicode__(self):
        return self.choice

    class Meta:
        verbose_name = "valg"
        verbose_name_plural = "valg"

    def vote(self, user):
        if not self.poll.user_has_voted(user):
            self.votes += 1
            self.save()
            self.poll.users_voted.add(user)
            return True
        else:
            return False

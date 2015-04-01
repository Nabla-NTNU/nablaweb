# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class UserHasVoted(Exception):
    pass


class PollManager(models.Manager):
    def current_poll(self):
        queryset = super(PollManager, self).get_queryset()
        return queryset.get(is_current=True)


class Poll(models.Model):
    question = models.CharField('Spørsmål', max_length=1000)
    creation_date = models.DateTimeField('Opprettet', auto_now_add=True)
    publication_date = models.DateTimeField('Publisert')
    added_by = models.CharField('Lagt til av', max_length=100)
    edit_date = models.DateTimeField('Sist endret', auto_now=True)
    is_current = models.BooleanField('Nåværende avstemning?', default=True)
    users_voted = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         verbose_name='Brukere som har stemt', editable=False,
                                         help_text="")

    objects = PollManager()

    def __unicode__(self):
        return self.question

    def save(self, *args, **kwargs):
        if self.is_current:
            Poll.objects.filter(is_current=True)\
                .exclude(pk=self.pk)\
                .update(is_current=False)
        super(Poll, self).save(*args, **kwargs)

    def get_total_votes(self):
        return sum([x.votes for x in self.choice_set.all()])

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
    added_by = models.CharField('Lagt til av', max_length=100,
                                help_text="Hvem som la til valget i avstemningen")

    def __unicode__(self):
        return self.choice

    class Meta:
        verbose_name = "valg"
        verbose_name_plural = "valg"

    def vote(self, user):
        if self.poll.user_has_voted(user):
            raise UserHasVoted(u"{user} has already voted on {poll}.".format(user=user, poll=self.poll))
        else:
            self.votes += 1
            self.save()
            self.poll.users_voted.add(user)

from django.db import models
import datetime

class Poll(models.Model):
    question = models.CharField('Spoersmaal', max_length=1000)
    creation_date = models.DateTimeField('Opprettet', auto_now_add=True)
    publication_date = models.DateTimeField('Publisert')
    edit_date = models.DatoTimeField('Sist endret', auto_now=True)
    def __unicode__(self):
        return self.question
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField('Navn paa valg', max_length=500)
    votes = models.IntegerField('Antall stemmer')
    added_by = models.CharField('Lagt til av', max_length=100) # Hvem som la til valget i avstemningen
    creation_date = models.DateTimeField('Opprettet', auto_now_add=True)
    hidden = models.BooleanField('Gjemt') # Hvorvidt valget er gjemt
    def __unicode__(self):
        return self.choice

# Create your models here.

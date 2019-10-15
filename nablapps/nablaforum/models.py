from django.db import models
from nablapps.accounts.models import NablaGroup, NablaUser


class Channel(models.Model):
    ''' Represents a channel in the forum '''
    nabla_group = models.ForeignKey(NablaGroup, on_delete=models.CASCADE)
    name = nabla_group.name
    description = models.TextField()


class Thread(models.Model):
    ''' Represents a thread in a channel'''
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE) #which channel it belongs to
    threadstarter = models.ForeignKey(NablaUser, on_delete=models.CASCADE) # lurt med CASCADE her eller?
    title = models.CharField(max_length=200)
    text_body = models.TextField()


class Message(models.Model):
    ''' Represents a message in a thread '''
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(NablaUser, on_delete=models.CASCADE)


#Suggestion: make abstract message class and make thread and message extend it



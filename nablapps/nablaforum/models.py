from django.db import models
from nablapps.accounts.models import NablaUser, NablaGroup

class Channel(models.Model):
    ''' Represents a channel in the forum '''
    #group = models.ForeignKey(NablaGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Thread(models.Model):
    ''' Represents a thread in a channel'''
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE) #which channel it belongs to
    threadstarter = models.ForeignKey(NablaUser, on_delete=models.CASCADE) # lurt med CASCADE her eller?
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title


class Message(models.Model):
    ''' Represents a message in a thread '''
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(NablaUser, on_delete=models.CASCADE,)
    message = models.TextField()

    def __str__(self):
        return self.user.username


#Suggestion: make abstract message class and make thread and message extend it



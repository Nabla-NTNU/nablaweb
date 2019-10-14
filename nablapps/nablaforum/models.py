from django.db import models


class Channel(models.Model):
    ''' Represents a channel in the forum '''
    name = models.CharField(max_length=200)
    description = models.TextField()
    #member_group = NablaGroup


class Thread(models.Model):
    ''' Represents a thread in a channel'''
    #channel = which channel it belongs to
    topic = models.CharField(max_length=200)
    message = models.TextField()
    #threadstarter = user from Channel member group


class Message(models.Model):
    ''' Represents a message in a thread '''
    #thread = bellonging thread
    #user = user from member group


#Suggestion: make abstract message class and make thread and message extend it



"""
Models for poll app


Some design info for the models
==================================

- A poll has multiple choices.
- A user can only answer once and can only pick a single choice.
- When a user has voted, it is not possible to see what they have voted for.
- A poll can either be created be created by staff or by a user. When it
  is created by a user it is called a user_poll and is listed along other user polls.
- A single poll can be set to be the current poll,
  which means it is the one to be shown on the front page.

"""
from django.conf import settings
from django.db import models
from random import shuffle


class UserHasVoted(Exception):
    """Raised if the user has already voted on a poll"""


class PollManager(models.Manager):
    """Django manager for Poll model"""

    def current_poll(self):
        """Gets the current poll"""
        queryset = super().get_queryset()
        return queryset.get(is_current=True)


class Poll(models.Model):
    """
    Model representing a poll.
    """

    question = models.CharField("Spørsmål", max_length=1000)

    answer = models.CharField("Svar", max_length=1000, default="", blank=True)

    creation_date = models.DateTimeField("Opprettet", auto_now_add=True)

    publication_date = models.DateTimeField("Publisert")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="poll_created_by",
        verbose_name="Lagt til av",
        editable=False,
        null=True,
        on_delete=models.CASCADE,
    )

    edit_date = models.DateTimeField("Sist endret", auto_now=True)

    is_current = models.BooleanField("Nåværende avstemning?", default=True)

    users_voted = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Brukere som har stemt",
        editable=False,
        help_text="",
    )

    is_user_poll = models.BooleanField("Er brukerpoll", editable=False, default=False)

    objects = PollManager()

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        if self.is_current:
            Poll.objects.filter(is_current=True).exclude(pk=self.pk).update(
                is_current=False
            )
        super().save(*args, **kwargs)

    def get_total_votes(self):
        """Return the sum of all votes for all choices"""
        return sum([x.votes for x in self.choices.all()])

    def user_has_voted(self, user):
        """Return whether the given user has voted on the poll"""
        return user in self.users_voted.all()

    def randomise_poll(self):
        self.shuffled = list(self.choices.all())
        shuffle(self.shuffled)
        return ''

    class Meta:
        verbose_name = "Avstemning"
        verbose_name_plural = "Avstemninger"


class Choice(models.Model):
    """
    Model representing a single choice for a single Poll instance
    """

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")

    choice = models.CharField("Navn på valg", max_length=80)

    votes = models.IntegerField("Antall stemmer", blank=False, default=0)

    creation_date = models.DateTimeField("Lagt til", auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="choice_created_by",
        verbose_name="Lagt til av",
        editable=False,
        help_text="Hvem som la til valget i avstemningen",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = "valg"
        verbose_name_plural = "valg"

    def vote(self, user):
        """
        Add a vote to the choice from the given user.
        An exception is raised if the user has already voted.
        """
        if self.poll.user_has_voted(user):
            raise UserHasVoted(f"{user} has already voted on {self.poll}.")
        else:
            self.votes += 1
            self.save()
            self.poll.users_voted.add(user)

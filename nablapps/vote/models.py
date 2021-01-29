from django.db import models
from django.conf import settings

"""
These models are esentially the same as in poll/models.
Code heavily boiled.
"""


class UserAlreadyVoted(Exception):
    """Raised if the voting user has already voted on a votation"""


class Votation(models.Model):
    """ Represents a votation """
    title = models.CharField(max_length=100)
    description = models.TextField()
    users_voted = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_voted")
    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="Votation_created_by",
            verbose_name="Opprettet av",
            editable=False,
            null=True,
            on_delete=models.CASCADE,
    )
    is_active = models.BooleanField("Åpen for avtemning?", default=False)


    def __str__(self):
        return self.title


    def user_already_voted(self, user):
        """ returns true if the given user has already voted """
        return user in self.users_voted


    def get_total_votes(self):
        """Return the sum of votes for all belonging alternatives"""
        return sum([alt.votes for alt in self.alternatives.all()])


    def activate(self):
        """Activates votation and opens for voting"""
        self.is_active = True
    

    def deactivate(self):
        """Deactivates votation and closes for voting"""
        self.is_active = False


class Alternative(models.Model):
    """ Represents an alternative """
    votation = models.ForeignKey(Votation, on_delete=models.CASCADE, related_name="alternatives")
    text = models.CharField(max_length=250)
    votes = models.IntegerField("Antall stemmer", blank=False, default=0)


    def __str__(self):
        return self.text


    def add_vote(self, user):
        """ Add users vote """
        if self.votation.user_already_voted(user):
            raise UserAlreadyVoted(f"{user} has already voted on {self.votation}.")
        else:
            self.votes =+ 1
            self.save()
            self.votation.users_voted.add(user)


    def get_vote_percentage(self):
        """Return the percentage of the total votes this alternative got"""
        if self.votation.get_total_votes() == 0:
            return 0
        else:
            return 100*self.votes/self.votation.get_total_votes()

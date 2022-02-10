import random

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from nablapps.accounts.models import NablaGroup

"""
These models are esentially the same as in poll/models.
Code heavily boiled.
"""


class VotingEvent(models.Model):
    title = models.CharField(max_length=100)
    creation_date = models.DateTimeField("Opprettet", auto_now_add=True)
    checked_in_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="checked_in_users", blank=True
    )
    users_should_poll = models.BooleanField(
        "Clients should poll for updates", default=False
    )
    require_checkin = models.BooleanField(
        "Users must check in to submit votes", default=True
    )
    eligible_group = models.ForeignKey(
        NablaGroup,
        on_delete=models.CASCADE,
        related_name="voting_events",
        blank=True,
        null=True,
    )

    def user_eligible(self, user):
        """Check if user i eligible for voting event."""
        if self.eligible_group is None:
            return True  # Empty group means no restrictions.
        return user.groups.filter(pk=self.eligible_group.pk).exists()

    def user_checked_in(self, user):
        return self.checked_in_users.filter(pk=user.pk).exists()

    def num_checked_in(self):
        return self.checked_in_users.count()

    def check_in_user(self, user, ignore_eligible=False):
        """Adds the user to the checked_in_users.
        If ignore_eligible, do not verify user is eligible.
        Raises UserNotEligible if not elible and ignore_eligible is false"""
        if ignore_eligible or self.user_eligible(user):
            self.checked_in_users.add(user)
            self.save()
        else:
            raise UserNotEligible

    def check_out_user(self, user):
        """Removes user form checked_in_users"""
        self.checked_in_users.remove(user)
        self.save()

    def check_out_all(self):
        """Check out all usesrs"""
        for user in self.checked_in_users.all():
            self.check_out_user(user)

    def toggle_check_in_user(self, user):
        """Toggle user checked in status.
        Throws UserNotEligible if user is not eligible"""
        if self.user_checked_in(user):
            self.check_out_user(user)
        else:
            self.check_in_user(user)

    class Meta:
        permissions = [
            ("vote_admin", "can administer voting"),
            ("vote_inspector", "can inspect voting"),
        ]

    def __str__(self):
        return self.title


class UserAlreadyVoted(Exception):
    """Raised if the voting user has already voted on a voting"""


class UserNotEligible(Exception):
    """Raised if the voting user is not eligible to vote.
    Note: this should not be used for users not being checked in,
    in which case UserNotCheckedIn should be used."""


class UserNotCheckedIn(Exception):
    """Raised if the voting user is not checked in for event with checkin"""


class VotingDeactive(Exception):
    """Raised if the user tries to vote on an inactive voting"""


class DuplicatePriorities(Exception):
    """Raised if users tries to submit a STV ballot with dubplicate canditate(s) accross priorities"""


class UnableToSelectWinners(Exception):
    """Raised if unable to select winners in multi winner election"""


class VoteDistributionError(Exception):
    """Raised if unable to find winners"""


class HoleInBallotError(Exception):
    """Raised empty priority in vote ballot followed by non empty entry encountered"""


class Voting(models.Model):
    """Represents a voting"""

    event = models.ForeignKey(
        VotingEvent, on_delete=models.CASCADE, related_name="votings"
    )
    title = models.CharField(max_length=100)
    num_winners = models.IntegerField(blank=False, default=1)
    description = models.TextField()
    users_voted = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="users_voted",
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="Voting_created_by",
        verbose_name="Opprettet av",
        editable=False,
        null=True,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField("Åpen for avtemning?", default=False)

    def __str__(self):
        return self.title

    def user_already_voted(self, user):
        """returns true if the given user has already voted"""
        return user in self.users_voted.all()

    def get_total_votes(self):
        """Return the sum of votes for all belonging alternatives"""
        return self.users_voted.all().count()

    def get_num_alternatives(self):
        """Returns the number of related/belinging alternatives"""
        return len(self.alternatives.all())

    def activate(self):
        """Activates voting and opens for voting"""
        self.is_active = True

    def deactivate(self):
        """Deactivates voting and closes for voting"""
        self.is_active = False

    def user_not_eligible(self, user):
        return not self.event.user_eligible(user)

    def is_preference_vote(self):
        """The voting uses preference vote, not 'radio' select"""
        return self.num_winners > 1

    def submit_stv_votes(self, user, ballot_dict):
        """Submits transferable votes i.e. creates ballot"""
        assert self.is_preference_vote(), "Only preference votes can have ballots"

        alt_pks = [int(ballot_dict[pri]) for pri in ballot_dict]
        if len(alt_pks) != len(set(alt_pks)):
            raise DuplicatePriorities("Ballot contains duplicate(s) of candidates")
        alt1_pk = int(ballot_dict[1])
        alt1 = self.alternatives.get(pk=alt1_pk)
        # create BallotContainer instance
        new_ballot = BallotContainer.objects.create(
            voting=self, current_alternative=alt1
        )
        new_ballot.save()
        # Create BallotEntry instances
        for (alt_pk, pri) in zip(alt_pks, ballot_dict):
            alt = Alternative.objects.get(pk=alt_pk)
            new_entry = BallotEntry.objects.create(
                container=new_ballot, priority=pri, alternative=alt
            )
            new_entry.save()
            self.users_voted.add(user)

    def multi_winnner_initial_dist(self):
        """Initial distribution of votes according to first priority"""
        for ballot in self.ballots.all():
            alt1 = ballot.entries.get(priority=1).alternative
            ballot.alternative = alt1
            ballot.save()

    def get_quota(self):
        """Returns the droop quota for a preference vote"""
        assert self.is_preference_vote(), "Only preference votes have quotas"
        return int(self.get_total_votes() / (self.num_winners + 1)) + 1

    def get_multi_winner_result(self):
        """Declare multples winners using a single transferable votes system"""
        assert self.is_preference_vote(), "Only preference votes can distribute votes"

        alternatives = self.alternatives.all()
        quota = self.get_quota()
        winners = []
        losers = []

        # Initial ballot/vote distribution according to first priority
        self.multi_winnner_initial_dist()

        # Find winners, transfer votes and eliminate losers if necessary
        if self.get_total_votes() < quota * self.num_winners:
            # Innsufficient vote count
            # Consider raising exception
            raise UnableToSelectWinners(
                f"Not enough votes to declare {self.num_winners} winners"
            )
        else:
            # Vote count is sufficient to declare winners

            # Loop through number of losing alternatives (max number of loser to eliminate)
            for i in range(len(alternatives) - self.num_winners):
                # Find winners, redistribute surpluses until no more winners found
                # If not enough winners are found, then proceed to loser elimination
                for j in range(self.num_winners):
                    new_winners = {}  # New winners found this round {alt: surplus}

                    # Find alternatives passing quota, add to winners
                    for alt in alternatives:
                        if alt in winners:
                            # Can't win twice
                            pass
                        elif alt.ballots.all().count() >= quota:
                            # declare alt as a winner, find surplus
                            num_surplus_votes = alt.ballots.all().count() - quota
                            new_winners[alt] = num_surplus_votes
                            winners.append(alt)
                    if len(winners) == self.num_winners:
                        # All winners found
                        return winners
                    if len(new_winners) == 0:
                        # No winners, need to eliminate loser
                        break

                    # Sort winners and surpluses in order of descending surplus
                    # Does this sorting matter?
                    new_winners_sorted = sorted(
                        new_winners.items(), key=lambda x: x[1], reverse=True
                    )  # List of tuples [(alt, num_surplus_votes),...]

                    for winner, surplus_count in new_winners_sorted:
                        # First find all transferable votes (non exhausted ballots)
                        winner_ballots = winner.ballots.all()
                        transferable_ballots = []
                        for ballot in winner_ballots:
                            pri = ballot.entries.get(alternative=winner).priority
                            if pri == ballot.entries.all().count():
                                # Ballot exhausted, not transferable
                                pass
                            else:
                                transferable_ballots.append(ballot)
                        # Then transfer surplus
                        if len(transferable_ballots) <= surplus_count:
                            # transfer all transferable_ballots
                            for ballot in transferable_ballots:
                                pri = ballot.entries.get(alternative=winner).priority
                                next_prioritezed_alt = ballot.entries.get(
                                    priority=pri + 1
                                ).alternative
                                ballot.current_alternative = next_prioritezed_alt
                                ballot.save()
                        else:
                            # Random sample N ballots from winners votes
                            redist_indices = random.sample(
                                range(len(transferable_ballots)), surplus_count
                            )
                            for i in redist_indices:
                                # For each selected ballot, transfer it to next priority alternative
                                ballot = transferable_ballots[i]
                                pri = ballot.entries.get(alternative=winner).priority
                                next_prioritezed_alt = ballot.entries.get(
                                    priority=pri + 1
                                ).alternative
                                ballot.alternative = next_prioritezed_alt
                                ballot.save()
                # out of inner loop
                # If not enough winners, eliminate 'biggest loser' and redistribute votes
                if len(winners) < self.num_winners:
                    # First find 'biggest' loser
                    # probably a more elegant way to do this
                    remaining_alts = [alt for alt in alternatives if alt not in winners]
                    remaining_alts = [
                        alt for alt in remaining_alts if alt not in losers
                    ]
                    loser = remaining_alts[0]
                    for alt in remaining_alts[1:]:
                        if loser.ballots.all().count() > alt.ballots.all().count():
                            loser = alt
                    losers.append(loser)

                    # Redistribute all losers votes (consider different method?)
                    for ballot in loser.ballots.all():
                        pri = ballot.entries.get(alternative=loser).priority
                        if pri == ballot.entries.all().count():
                            # Ballot exhausted, not transferable
                            pass
                        else:
                            next_prioritezed_alt = ballot.entries.get(
                                priority=pri + 1
                            ).alternative
                            ballot.alternative = next_prioritezed_alt
                            ballot.save()
                    if self.num_winners - len(winners) == alternatives.count() - len(
                        losers
                    ) - len(winners):
                        # Declare remainders as winners
                        remaining_alts = [
                            alt for alt in alternatives if alt not in winners
                        ]
                        remaining_alts = [
                            alt for alt in remaining_alts if alt not in losers
                        ]
                        winners += remaining_alts
                        return winners
                elif len(winners) == self.num_winners:
                    return winners
                else:
                    raise VoteDistributionError(f"To many winners: {winners}")
            # outside of outer loop
            # Should really not make it here, so maybe throw exception instead
            if len(winners) == self.num_winners:
                return winners
            elif len(winners) > self.num_winners:
                raise VoteDistributionError(f"To many winners: {winners}")
            else:
                raise VoteDistributionError(
                    f"To few winners: {winners}, loser: {losers}"
                )


class Alternative(models.Model):
    """Represents an alternative"""

    voting = models.ForeignKey(
        Voting, on_delete=models.CASCADE, related_name="alternatives"
    )
    text = models.CharField(max_length=250)
    votes = models.IntegerField("Antall stemmer", blank=False, default=0)

    def __str__(self):
        return self.text

    def add_vote(self, user):
        """Add users vote"""
        assert not self.voting.is_preference_vote()

        if self.voting.user_already_voted(user):
            raise UserAlreadyVoted(f"{user} has already voted on {self.voting}.")
        elif self.voting.user_not_eligible(user):
            raise UserNotEligible(f"{user} is not eligible to vote on {self.voting}")
        elif (
            self.voting.event.require_checkin
            and not self.voting.event.user_checked_in(user)
        ):
            raise UserNotCheckedIn(f"{user} is not checked to event.")
        elif not self.voting.is_active:
            raise VotingDeactive(f"The voting {self.voting} is no longer open.")
        else:
            self.votes += 1
            self.save()
            self.voting.users_voted.add(user)

    def get_num_votes(self):
        """Returns the number of received votes

        Works for both preference and non-preference votes, and should
        be used instead of accessing the votes field directly."""
        if self.voting.is_preference_vote():
            return self.voting.ballots.filter(current_alternative=self).count()
        else:
            return self.votes

    def get_vote_percentage(self):
        """Return the percentage of the total votes this alternative got"""
        try:
            return 100 * self.get_num_votes() / self.voting.get_total_votes()
        except ZeroDivisionError:
            return 0


class BallotContainer(models.Model):
    """
    Dictonary like model storing ballot with priority and alternative

    E.g. for

    Voter A:
        {1: alt2, 2:alt1, 3:alt3}

    has alt2 as first choice, alt1 as second choice and alt3 as third choice
    """

    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name="ballots")
    current_alternative = models.ForeignKey(
        Alternative,
        on_delete=models.CASCADE,
        related_name="ballots",
        null=True,
        blank=True,
    )

    def clean(self):
        # Make sure all alternatives belong to voting
        votings = self.entries.values_list("alternative__voting", flat=True)
        if votings.filter(pk=self.voting.pk).Count() != votings.Count():
            raise ValidationError("All entries must belong to the voting.")


class BallotEntry(models.Model):
    """priority and # 'votes' as key:value"""

    container = models.ForeignKey(
        BallotContainer, on_delete=models.CASCADE, related_name="entries"
    )
    priority = models.IntegerField(validators=[MinValueValidator(1)])
    alternative = models.ForeignKey(Alternative, on_delete=models.CASCADE)

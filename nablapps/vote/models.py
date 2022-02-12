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
    is_preference_vote = models.BooleanField("Preferansevalg", default=False)

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

    def submit_stv_votes(self, user, ballot_dict):
        """
        Submits transferable votes i.e. creates ballot

        parameters:
            user: NablaUser (who sumbitted the vote)
            ballot_dict: dictionary with priority as keys, alternative.pk (id) as values

        ballot_dict = {} => Empty ballot (blank vote)
        """
        assert self.is_preference_vote, "Only preference votes can have ballots"

        self.users_voted.add(user)
        if ballot_dict == {}:
            # Empty ballot == blank vote
            # Then adding user to self.users_voted is sufficient
            # Do not create BallotContainer instance
            # Blank votes affects the quota
            return

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

        # Reset ballots/stv-results
        for alt in self.alternatives.all():
            alt.is_winner = False
            # Inital dist is called in the stv procedure, but could perhaps
            # consider calling it here too

    def multi_winnner_initial_dist(self):
        """Initial distribution of votes according to first priority"""
        for ballot in self.ballots.all():
            alt1 = ballot.entries.get(priority=1).alternative
            ballot.current_alternative = alt1
            ballot.save()

    def get_quota(self):
        """Returns the droop quota for a preference vote"""
        assert self.is_preference_vote, "Only preference votes have quotas"
        return int(self.get_total_votes() / (self.num_winners + 1)) + 1

    def _set_winners(self, winners):
        """Takes a list of winners, sets is_winner true for the winner"""
        for winner in winners:
            assert winner.voting == self  # make sure we don't alter another voting
            winner.is_winner = True
            winner.save()

    def _transfer_ballot(self, ballot, current_alt):
        """
        Transfers vote to next priority on the ballot
        the given ballot must be transferable, i.e. not exhausted
        i.e. not already be assigned to it's last priority
        """
        assert ballot.voting == self  # Don't mess with other's alternatives!
        pri = ballot.entries.get(alternative=current_alt).priority
        if pri == ballot.entries.all().count():
            return
        next_prioritezed_alt = ballot.entries.get(priority=pri + 1).alternative
        ballot.current_alternative = next_prioritezed_alt
        ballot.save()

    def stv_find_winners(self):
        """Declare multples winners using a single transferable votes system"""
        assert self.is_preference_vote, "Only preference votes can distribute votes"

        alternatives = self.alternatives.all()
        quota = self.get_quota()  # Number of votes to be declared winner
        winners = []  # Alternatives that are declared winners
        losers = []  # Alternatives that are eliminated as losers
        num_non_blank_ballots = self.ballots.all().count()

        assert not (
            len(alternatives) == 1 and self.num_winners == 1
        ), "Preference vote should not be used for one alternative and one winner"

        # Initial ballot/vote distribution according to first priority
        self.multi_winnner_initial_dist()

        num_losers = len(alternatives) - self.num_winners
        if num_losers < 0:
            # Not enough alternatives/candidates
            raise UnableToSelectWinners(
                f"Not enough alternatives(candidates) to declare {self.num_winners} winners"
            )
        elif num_losers > 0:
            # More candidates than winners
            # Need enough votes declare by passing quota or by elimination
            if num_non_blank_ballots < self.num_winners:
                # Then at least one seat will be ambigous
                raise UnableToSelectWinners(
                    f"Not enough votes to declare {self.num_winners} winners"
                )
        else:  # num_losers == 0:
            # Everyone wins, regardless of vote count
            # If all alternatives pass the quota -> end voting, don't transfer votes
            # If only some are past the quota -> redistribute surplus(es)
            # If no one is past the quota -> no surpluses -> end voting
            winners_default = list(
                alternatives
            )  # Not sure if needed or sensible to convert to list
            num_past_quota = 0
            num_below_quota = 0
            for winner in winners_default:
                if winner.ballots.all().count() < quota:
                    num_below_quota += 1
                else:
                    num_past_quota += 1
            # If both if test below are false only some are past quota -> transfer surplus
            if num_below_quota == 0:
                # Everyone past quota after inital distribution, nice, no transfer
                # assert num_past_quota == self.num_winners
                return winners_default
            elif num_past_quota == 0:
                # assert num_below_quota == self.num_winners
                # No one passes quota, not nice, but still no transfer
                return winners_default

        # Find winners, transfer votes and eliminate losers if necessary
        # Loop through number of losing alternatives (max number of loser to eliminate)
        # If num_losers == 0, run loop one time to distribute surplus votes
        for i in range(max(num_losers, 1)):
            # Find winners, redistribute surpluses until no more winners found
            # If not enough winners are found, then proceed to loser elimination
            for j in range(self.num_winners):
                past_quota_votes = {}  # {alt: votes} # votes at the time of counting
                found_new_winners = False
                # Find alternatives passing quota, add to winners (if not already winner)
                for alt in alternatives:
                    if alt.ballots.all().count() >= quota:
                        # add to past quoata dict for future surplus transfer
                        # if not already winner, add to winners and new_winners
                        past_quota_votes[alt] = alt.ballots.all()
                        if alt not in winners:
                            # Can't win twice, only add to winner if not already winner
                            winners.append(alt)
                            found_new_winners = True
                if len(winners) == self.num_winners:
                    # All winners found
                    # All winners past quota
                    # Voting procedure is done
                    return winners
                elif len(winners) > self.num_winners:
                    raise VoteDistributionError(f"Too many winners: {winners}")
                if not found_new_winners:
                    # No new winners, still free 'seats', need to eliminate loser
                    break
                # Transfer surplus of all winners, old and new
                for winner, winner_ballots in past_quota_votes.items():
                    # Find size of surplus and the transferable votes at time of counting
                    # Distribute surplus from the votes at the time of counting
                    surplus_count = winner_ballots.count() - quota
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
                            self._transfer_ballot(ballot, winner)
                    else:
                        # Random sample N ballots from winners transferable_ballots
                        redist_indices = random.sample(
                            range(len(transferable_ballots)), surplus_count
                        )
                        for i in redist_indices:
                            # For each selected ballot, transfer it to next priority alternative
                            self._transfer_ballot(transferable_ballots[i], winner)
            # out of inner loop
            # If not enough winners, eliminate 'biggest loser' and redistribute votes
            if num_losers == 0:
                # No one to eliminate, declare everyone as winners
                # Surpluses has been transfered
                winners = list(alternatives)  # again, maybe list conversion is stupid
                return winners
            if len(winners) < self.num_winners:
                # First find 'biggest' loser
                # probably a more elegant way to do this
                remaining_alts = [alt for alt in alternatives if alt not in winners]
                remaining_alts = [alt for alt in remaining_alts if alt not in losers]
                vote_counts = {alt: alt.ballots.all().count() for alt in remaining_alts}
                sorted_by_vote_counts = sorted(vote_counts, key=vote_counts.get)
                first_loser = sorted_by_vote_counts[0]
                second_loser = sorted_by_vote_counts[1]
                first_loser_vote_count = first_loser.ballots.all().count()
                second_loser_vote_count = second_loser.ballots.all().count()
                if first_loser_vote_count < second_loser_vote_count:
                    # First loser is the sole loser, eliminate
                    print("Found unique loser")
                    loser = first_loser
                elif first_loser_vote_count == second_loser_vote_count:
                    # Two or more losers with same amount of votes
                    # End procedure, return the already found winners
                    print("Cannot eliminate")
                    print("Exiting")
                    return winners
                else:
                    # Should not happen
                    raise VoteDistributionError(
                        "First loser has more votes than second. Error in implementation."
                    )
                losers.append(loser)
                # Redistribute all losers votes
                for ballot in loser.ballots.all():
                    self._transfer_ballot(ballot, loser)
                if self.num_winners - len(winners) == alternatives.count() - len(
                    losers
                ) - len(winners):
                    # Declare remainders as winners
                    remaining_alts = [alt for alt in alternatives if alt not in winners]
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
            raise VoteDistributionError(f"To few winners: {winners}, loser: {losers}")

    # Maybe rename since it can be used also when there is one winner
    def get_multi_winner_result(self):
        winners = self.stv_find_winners()
        self._set_winners(winners)
        return winners

    @property
    def winners(self):
        return self.alternatives.filter(is_winner=True)


class Alternative(models.Model):
    """Represents an alternative"""

    voting = models.ForeignKey(
        Voting, on_delete=models.CASCADE, related_name="alternatives"
    )
    text = models.CharField(max_length=250)
    votes = models.IntegerField("Antall stemmer", blank=False, default=0)
    is_winner = models.BooleanField("Alternative is declared winner", default=False)

    def __str__(self):
        return self.text

    def add_vote(self, user):
        """Add users vote"""
        assert not self.voting.is_preference_vote

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
        if self.voting.is_preference_vote:
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

import json
import unittest
from contextlib import nullcontext
from unittest import skip

from django.contrib.auth.models import Permission
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from nablapps.accounts.models import NablaGroup, NablaUser

from .models import (
    Alternative,
    DuplicatePriorities,
    UnableToSelectWinners,
    UserAlreadyVoted,
    UserNotCheckedIn,
    UserNotEligible,
    VoteDistributionError,
    Voting,
    VotingDeactive,
    VotingEvent,
)

"""Notes for file:
TODO: Tests of login required and user permissions for endpoints (API and views)
TODO: Other tests of views. (Now we only test models)
TODO: Change naming from 'eligible' to 'eligible_group', or similar. Now it
      can be a source of confusion whether eligible refers to being in the eligible group
      or also being checked in.
"""


#################
## Model tests ##
#################
class CheckinTestCase(TestCase):
    """Check functionality related to checkin.

    Discussion:
    There are several restrictions we may have on wether or not users may cast a vote.
    We can have either have checkin, eligeble groups, or a combination where the user must both check in and be part of the group.
    """

    def setUp(self):
        self.group1 = NablaGroup.objects.create(name="Group 1")
        self.group2 = NablaGroup.objects.create(name="Group 2")
        self.user0 = NablaUser.objects.create_user(
            username="userNoGroup",
        )
        self.user1 = NablaUser.objects.create_user(
            username="user1",
        )
        self.user1.groups.add(self.group1)
        self.user2 = NablaUser.objects.create_user(
            username="user2",
        )
        self.user2.groups.add(self.group2)
        self.voting_event0 = VotingEvent.objects.create(
            title="Voting_Event event for all",
        )
        self.voting_event1 = VotingEvent.objects.create(
            title="Voting_Event event for group1",
            eligible_group=self.group1,
        )
        self.voting_event2 = VotingEvent.objects.create(
            title="Voting_Event event for group1",
            eligible_group=self.group2,
        )

    def test_check_in_user_eligible_group(self):
        # Test logging in user to event, should fail/succed
        tests = [
            {"user": self.user0, "voting_event": self.voting_event0, "succeed": True},
            {"user": self.user0, "voting_event": self.voting_event1, "succeed": False},
            {"user": self.user1, "voting_event": self.voting_event0, "succeed": True},
            {"user": self.user1, "voting_event": self.voting_event1, "succeed": True},
            {"user": self.user1, "voting_event": self.voting_event2, "succeed": False},
        ]
        for test in tests:
            if test["succeed"]:
                test["voting_event"].check_in_user(test["user"])
                self.assertIn(test["user"], test["voting_event"].checked_in_users.all())
            else:
                with self.assertRaises(UserNotEligible):
                    test["voting_event"].check_in_user(test["user"])
                self.assertNotIn(
                    test["user"], test["voting_event"].checked_in_users.all()
                )

    def test_check_in_out_user(self):
        """Test that user check out works"""
        # Check in and out
        self.voting_event0.check_in_user(self.user0)
        self.assertIn(self.user0, self.voting_event0.checked_in_users.all())
        self.voting_event0.check_out_user(self.user0)
        self.assertNotIn(self.user0, self.voting_event0.checked_in_users.all())

        # Check in twice, should give no error
        self.voting_event0.check_in_user(self.user0)
        self.voting_event0.check_in_user(self.user0)
        self.assertIn(self.user0, self.voting_event0.checked_in_users.all())

        # Check out twice, should not give error
        self.voting_event0.check_out_user(self.user0)
        self.voting_event0.check_out_user(self.user0)
        self.assertNotIn(self.user0, self.voting_event0.checked_in_users.all())

        # Check toggle
        # Note that the user is now checked out
        self.voting_event0.toggle_check_in_user(self.user0)
        self.assertIn(self.user0, self.voting_event0.checked_in_users.all())
        self.voting_event0.toggle_check_in_user(self.user0)
        self.assertNotIn(self.user0, self.voting_event0.checked_in_users.all())

    def test_check_out_all(self):
        """Check that check out all users work"""
        self.voting_event0.check_out_all()  # Check out with empty event should not cause exception

        # Add some users
        for user in [self.user0, self.user1, self.user2]:
            self.voting_event0.check_in_user(user)
        self.voting_event0.check_out_all()
        # Check for empty. exists False when empty..
        self.assertFalse(self.voting_event0.checked_in_users.exists())


class SubmitVoteTestCase(TransactionTestCase):
    """Tests of submitting votes"""

    def setUp(self):
        self.group1 = NablaGroup.objects.create(name="Group 1")
        self.user0 = NablaUser.objects.create_user(
            username="userNoGroup",
        )
        self.user1 = NablaUser.objects.create_user(
            username="user1",
        )
        self.user1.groups.add(self.group1)
        self.user2 = NablaUser.objects.create_user(
            username="user2",
        )
        self.user2.groups.add(self.group1)
        self.voting_event0 = VotingEvent.objects.create(
            title="Voting event for all",
            require_checkin=False,
        )
        self.voting_event1 = VotingEvent.objects.create(
            title="Voting event for group1",
            eligible_group=self.group1,
            require_checkin=False,
        )

        self.voting0 = Voting.objects.create(
            event=self.voting_event0,
            is_active=True,
        )
        self.voting1 = Voting.objects.create(
            event=self.voting_event1,
            is_active=True,
        )

        self.voting0_alternative0 = Alternative.objects.create(
            voting=self.voting0,
            text="First alternative voting 0",
        )
        self.voting1_alternative0 = Alternative.objects.create(
            voting=self.voting1,
            text="First alternative voting 1",
        )

        self.preference_voting = Voting.objects.create(
            event=self.voting_event1,
            is_preference_vote=True,
            is_active=True,
        )
        for i in range(3):
            setattr(
                self,
                f"preference_vote_alternative{i}",
                Alternative.objects.create(
                    voting=self.preference_voting, text=f"Preference vote alt {i}"
                ),
            )

    @skip("Test cannot deal with blocking transaction")
    def test_submit_vote(self):
        """Submit a vote, check that counter increases"""
        self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 1)

    @skip("Test cannot deal with blocking transaction")
    def test_submit_preference_vote(self):
        """Submit a preference vote"""
        # TODO check that we get the correct result?

        cases = [
            {
                # Unfilled, i.e. blank
                "preferences": {},
                "expected_exception": None,
            },
            {
                # Partially filled preferences
                "preferences": {
                    1: self.preference_vote_alternative0,
                    2: self.preference_vote_alternative2,
                },
                "expected_exception": None,
            },
            {
                # Duplicate "preferences"
                "preferences": {
                    1: self.preference_vote_alternative0,
                    2: self.preference_vote_alternative0,
                },
                "expected_exception": DuplicatePriorities,
            },
            {
                # Same priority repeated
                "preferences": {
                    1: self.preference_vote_alternative0,  # noqa: F601
                    1: self.preference_vote_alternative1,  # noqa: F601
                },
                "expected_exception": DuplicatePriorities,
            },
        ]
        for case in cases:
            # Clean
            self.preference_voting.users_voted.clear()
            self.preference_voting.ballots.all().delete()
            exception = case["expected_exception"]
            # If we do not expect exception, make a null context manager as a placeholder
            contextManager = (
                nullcontext() if exception is None else self.assertRaises(exception)
            )
            with contextManager:
                ballot = {
                    pri: alternative.pk
                    for pri, alternative in case["preferences"].items()
                }
                self.preference_voting.submit_stv_votes(self.user1, ballot)

    def _submit_preference_vote(self, user=None):
        """Submit a partial ballot for user"""
        if user is None:
            user = self.user1
        preferences = {
            1: self.preference_vote_alternative0.pk,
            2: self.preference_vote_alternative2.pk,
        }
        self.preference_voting.submit_stv_votes(user, preferences)

    @skip("Test cannot deal with blocking transaction")
    def test_submit_non_active_vote(self):
        """Submit a vote on non-open voting"""
        self.voting0.is_active = False
        with self.assertRaises(VotingDeactive):
            self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 0)

        self.preference_voting.is_active = False
        with self.assertRaises(VotingDeactive):
            self._submit_preference_vote()
        # Make sure no ballot was created
        self.assertFalse(self.preference_voting.ballots.exists())

    def test_submit_noneligible_vote(self):
        """Submit a vote for which the user is not eligible"""
        with self.assertRaises(UserNotEligible):
            self.voting1_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting1_alternative0.votes, 0)

        with self.assertRaises(UserNotEligible):
            self._submit_preference_vote(user=self.user0)
        # Make sure no ballot was created
        self.assertFalse(self.preference_voting.ballots.exists())

    @skip("Test cannot deal with blocking transaction")
    def test_submit_second_vote(self):
        """Submit a second vote"""
        self.voting0_alternative0.add_vote(self.user0)
        with self.assertRaises(UserAlreadyVoted):
            self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 1)

        self._submit_preference_vote()
        with self.assertRaises(UserAlreadyVoted):
            self._submit_preference_vote()
        # Make sure no extra ballot was created
        self.assertEqual(
            self.preference_voting.ballots.count(),
            1,
        )

    @skip("Test cannot deal with blocking transaction")
    def test_checkin(self):
        """Submit a vote, depending on whether checked in or not, should succeed/fail"""
        self.voting_event0.require_checkin = True
        self.voting_event0.save()
        self.voting_event0.check_in_user(self.user0)
        self.voting0_alternative0.add_vote(self.user0)
        self.voting0_alternative0.refresh_from_db()
        self.assertEqual(self.voting0_alternative0.votes, 1)
        with self.assertRaises(UserNotCheckedIn):
            self.voting0_alternative0.add_vote(self.user1)  # Has not checked in
        self.assertEqual(self.voting0_alternative0.votes, 1)

        self.voting_event1.require_checkin = True
        self.voting_event1.save()
        self.voting_event1.check_in_user(self.user1)
        self._submit_preference_vote()
        self.assertEqual(
            self.preference_voting.ballots.count(),
            1,
        )
        with self.assertRaises(UserNotCheckedIn):
            self._submit_preference_vote(self.user2)
        self.assertEqual(
            self.preference_voting.ballots.count(),
            1,
        )


class PreferenceVoteDistributionTestCase(TestCase):
    """Tests of distributinos of preference votes"""

    num_users = 5

    def setUp(self):
        self.voting_event0 = VotingEvent.objects.create(
            title="Voting event for all",
            require_checkin=False,
        )
        for i in range(self.num_users):
            user = NablaUser.objects.create_user(
                username=f"user{i}",
            )
            setattr(self, f"user{i}", user)

        self.preference_voting = Voting.objects.create(
            event=self.voting_event0,
            is_preference_vote=True,
            is_active=True,
        )

    def test_distribute_vote(self):
        """Distrubute various configurations of votes"""
        tests = []

        def _get_ballot(n):
            return {i + 1: i + 1 for i in range(n)}

        for num_alternatives in range(1, 4):
            for num_winners in range(1, num_alternatives + 1):
                for num_voters in range(0, self.num_users):
                    if num_winners == 1 and num_alternatives == 1:
                        # Should use normal voting
                        exception = AssertionError
                    elif num_winners == 1 and num_alternatives == 2:
                        # Should use normal voting
                        exception = AssertionError
                    elif num_alternatives < num_winners:
                        # Not enough alternatives to delcare num_winners winners
                        exception = UnableToSelectWinners
                    elif num_winners == num_alternatives:
                        # More than one winner, same amount of alternatives
                        # Everyone wins, like an acclamation, but surpluses are transfered
                        exception = None
                    elif num_voters == 0:
                        # num_alternatives > num_winners
                        exception = UnableToSelectWinners
                    else:
                        exception = None
                    tests.append(
                        {
                            "num_winners": num_winners,
                            "num_alternatives": num_alternatives,
                            # TODO: Should probably add non-filled ballots
                            "ballots": [
                                _get_ballot(num_alternatives) for i in range(num_voters)
                            ],
                            "expected_exception": exception,
                        }
                    )

        for test in tests:
            # Clean up
            self.preference_voting.ballots.all().delete()
            self.preference_voting.alternatives.all().delete()
            self.preference_voting.users_voted.clear()
            self.preference_voting.num_winners = test["num_winners"]
            self.preference_voting.save()

            for i in range(test["num_alternatives"]):
                setattr(
                    self,
                    f"preference_vote_alternative{i}",
                    Alternative.objects.create(
                        voting=self.preference_voting, text=f"Preference vote alt {i}"
                    ),
                )

            starting_pk = self.preference_voting.alternatives.first().pk
            for i, ballot in enumerate(test["ballots"]):
                user = getattr(self, f"user{i}")
                ballot = {i: j + starting_pk - 1 for i, j in ballot.items()}
                self.preference_voting.submit_stv_votes(user, ballot)
            exception = test["expected_exception"]
            contextManager = (
                nullcontext()
                if exception is None
                else self.assertRaises(exception, msg=test)
            )
            # Temporarily disable errors, so that we can run through them all
            with contextManager:
                self.preference_voting.get_multi_winner_result()


################
## View tests ##
################


class ViewTestCase(TestCase):
    def setUp(self):
        vote_staff = NablaGroup.objects.create(name="vote_staff")
        vote_staff.permissions.add(Permission.objects.get(codename="vote_inspector"))
        users = [
            # [username, password, superuser, groups]
            ["admin", "admin", True, None],
            ["bob", "bob", False, [vote_staff]],
            ["alice", "alice", False, None],
        ]
        for user in users:
            username, password, superuser, groups = user
            new_user = NablaUser.objects.create_user(
                username=username,
                password=password,
                is_superuser=superuser,
                is_staff=superuser,
            )
            if groups is not None:
                new_user.groups.add(*groups)
            setattr(self, f"{username}_user", new_user)

        self.voting_event0 = VotingEvent.objects.create(
            title="Voting event for all",
        )
        self.voting0 = Voting.objects.create(
            event=self.voting_event0,
            is_active=True,
        )
        self.voting1 = Voting.objects.create(
            event=self.voting_event0,
            is_active=True,
        )

        self.voting0_alternative0 = Alternative.objects.create(
            voting=self.voting0,
            text="First alternative voting 0",
        )
        self.voting0_alternative1 = Alternative.objects.create(
            voting=self.voting0,
            text="Second alternative voting 0",
        )
        self.voting0_alternative1 = Alternative.objects.create(
            voting=self.voting0,
            text="Third alternative voting 0",
        )

    def test_permissions(self):
        admin = Client()
        assert admin.login(
            username=self.admin_user.username, password=self.admin_user.username
        )
        bob = Client()  # Inspector
        assert bob.login(
            username=self.bob_user.username, password=self.bob_user.username
        )
        alice = Client()
        assert alice.login(
            username=self.alice_user.username, password=self.alice_user.username
        )
        not_logged_in = Client()

        # Defines clients with expected status codes
        # Define one list for each 'type' of permission
        # class you want to test.
        clients_admin = [
            {"user": alice, "expected_code": 403},
            {"user": bob, "expected_code": 403},
            {"user": admin, "expected_code": 200},
            {"user": not_logged_in, "expected_code": 403},
        ]
        clients_inspector = [
            {"user": alice, "expected_code": 403},
            {"user": bob, "expected_code": 200},
            {"user": admin, "expected_code": 200},
            {"user": not_logged_in, "expected_code": 403},
        ]
        clients_public = [
            {"user": alice, "expected_code": 200},
            {"user": bob, "expected_code": 200},
            {"user": admin, "expected_code": 200},
            {"user": not_logged_in, "expected_code": 403},
        ]

        # Make some tests, represented by dicts, which calls various
        # views, and checks that we get rejected if we do not have
        # the proper rights.

        api_tests_setup = [
            ["api-public-votings", clients_public, {"pk": 1}, "get"],
            ["api-vote-event", clients_inspector, {"pk": 1}, "get"],
            ["api-users", clients_inspector, {"pk": 1}, "get"],
            ["api-votings", clients_inspector, {"pk": 1}, "get"],
        ]

        # I think we will remove some of these views in the future, but for now
        # we must test them.
        other_tests_setup = [
            ["voting-event-list", clients_inspector, {}, "get"],
            ["voting-list", clients_inspector, {"pk": 1}, "get"],
            ["register", clients_inspector, {"pk": 1}, "get"],
            ["create-voting", clients_inspector, {"pk": 1}, "get"],
            ["create-voting", clients_admin, {"pk": 1}, "post"],
            ["voting-edit", clients_inspector, {"pk": 1}, "get"],
            ["voting-edit", clients_admin, {"pk": 1}, "post"],
            ["voting-event-user", clients_public, {"pk": 1}, "get"],
            ["vote-event-list", clients_public, {}, "get"],
        ]

        tests_setup = api_tests_setup + other_tests_setup

        tests = [
            {
                "url": reverse(view, kwargs=kwargs),
                "view_name": view,
                "method": method,
                "data": {},
                "clients": client_group,
            }
            for view, client_group, kwargs, method in tests_setup
        ]

        for test in tests:
            for client in test["clients"]:
                method = getattr(client["user"], test["method"])
                response = method(test["url"])
                try:
                    self.assertEqual(
                        response.status_code,
                        client["expected_code"],
                        f"Wrong permissions for view {test['view_name']}. Failed for user {response.wsgi_request.user}.",
                    )
                except AssertionError as e:
                    # If we get a redirect (302) handle that as success if
                    # we expected to get 200.
                    if response.status_code == 302 and client["expected_code"] == 200:
                        pass
                    # If we get a redirect (302) to login when expecting rejection, it is fine
                    elif (
                        response.status_code == 302
                        and client["expected_code"] == 403
                        and response.url.startswith("/login/")
                    ):
                        pass
                    else:
                        raise e

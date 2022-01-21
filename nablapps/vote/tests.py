import unittest

from django.test import TestCase

from nablapps.accounts.models import NablaGroup, NablaUser

from .models import (
    Alternative,
    UserAlreadyVoted,
    UserNotCheckedIn,
    UserNotEligible,
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

    @unittest.skip("check_out_all not implemented yet")
    def test_check_out_all(self):
        """Check that check out all users work"""
        for user in [self.user0, self.user1, self.user2]:
            # self.voting_event0.check_in_user(user)
            pass

        self.voting_event0.check_out_all()
        # Check for empty. exists False when empty..
        self.assertFalse(self.voting_event0.checked_in_users.exists())


class SubmitVoteTestCase(TestCase):
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
        self.voting_event0 = VotingEvent.objects.create(
            title="Voting event for all",
        )
        self.voting_event1 = VotingEvent.objects.create(
            title="Voting event for group1",
            eligible_group=self.group1,
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

    def test_submit_vote(self):
        """Submit a vote, check that counter increases"""
        self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 1)

    def test_submit_non_active_vote(self):
        """Submit a vote on non-open voting"""
        self.voting0.is_active = False
        with self.assertRaises(VotingDeactive):
            self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 0)

    def test_submit_noneligible_vote(self):
        """Submit a vote for which the user is not eligible"""
        with self.assertRaises(UserNotEligible):
            self.voting1_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting1_alternative0.votes, 0)

    def test_submit_second_vote(self):
        """Submit a second vote"""
        self.voting0_alternative0.add_vote(self.user0)
        with self.assertRaises(UserAlreadyVoted):
            self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 1)

    def test_checkin(self):
        """Submit a vote, depending on whether checked in or not, should succeed/fail"""
        self.voting_event0.check_in_user(self.user0)
        self.voting0_alternative0.add_vote(self.user0)
        self.assertEqual(self.voting0_alternative0.votes, 1)
        with self.assertRaises(UserNotCheckedIn):
            self.voting0_alternative0.add_vote(self.user1)  # Has not checked in
        self.assertEqual(self.voting0_alternative0.votes, 1)

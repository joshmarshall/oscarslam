import unittest

from oscarslam import config
from oscarslam.categories import CATEGORIES
from oscarslam.models.user import User
from oscarslam.models.votes import Votes
from oscarslam.models.winner import Winner
from tests.helpers import FakeStore


class TestWinner(unittest.TestCase):

    def setUp(self):
        super(TestWinner, self).setUp()
        self.store = FakeStore()
        self.user = self.store.create(
            User, name="Foo Bar", email="foo@bar.com", password="whatever")

        self.categories = CATEGORIES.contest(config.CONTEST_ID)
        self.winner = self.store.create(Winner, contest=config.CONTEST_ID)
        self.winner.add_winner(
            self.categories[0].key, self.categories[0].nominees[0].key)
        self.winner.add_winner(
            self.categories[1].key, self.categories[1].nominees[1].key)

    def test_winner(self):
        self.assertEqual(2, len(self.winner.winners))
        self.assertEqual(self.winner.progress, 2.0 / len(self.categories))

    def test_winner_points(self):
        votes = Votes(email=self.user.email, contest=config.CONTEST_ID)
        votes.add_vote(
            self.categories[0].key, self.categories[0].nominees[0].key)
        votes.add_vote(
            self.categories[1].key, self.categories[1].nominees[0].key)

        points = self.winner.get_points(votes)
        self.assertEqual(self.categories[0].points, points)

        missed_points = self.winner.get_missed_points(votes)
        self.assertEqual(self.categories[1].points, missed_points)

        self.assertEqual(
            sum([c.points for c in self.categories][2:]),
            self.winner.remaining_points)

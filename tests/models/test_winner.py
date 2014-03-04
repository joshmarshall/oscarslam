from tests.helpers import FakeStore
from oscarslam.categories import CATEGORIES
from oscarslam.models.user import User
from oscarslam.models.votes import Votes
from oscarslam.models.winner import Winner
import unittest


class TestWinner(unittest.TestCase):

    def setUp(self):
        super(TestWinner, self).setUp()
        self.store = FakeStore()
        self.user = self.store.create(
            User, name="Foo Bar", email="foo@bar.com", password="whatever")

        self.winner = self.store.create(Winner, contest="oscars14")
        self.winner.add_winner(
            CATEGORIES[0].key, CATEGORIES[0].nominees[0].key)
        self.winner.add_winner(
            CATEGORIES[1].key, CATEGORIES[1].nominees[1].key)

    def test_winner(self):
        self.assertEqual(2, len(self.winner.winners))
        self.assertEqual(self.winner.progress, 2.0 / len(CATEGORIES))

    def test_winner_points(self):
        votes = Votes(email=self.user.email)
        votes.add_vote(CATEGORIES[0].key, CATEGORIES[0].nominees[0].key)
        votes.add_vote(CATEGORIES[1].key, CATEGORIES[1].nominees[0].key)

        points = self.winner.get_points(votes)
        self.assertEqual(CATEGORIES[0].points, points)

        missed_points = self.winner.get_missed_points(votes)
        self.assertEqual(CATEGORIES[1].points, missed_points)

        self.assertEqual(
            sum([c.points for c in CATEGORIES][2:]),
            self.winner.remaining_points)

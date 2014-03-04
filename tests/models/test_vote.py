from tests.helpers import FakeStore
from oscarslam.categories import CATEGORIES
from oscarslam.models.user import User
from oscarslam.models.votes import Votes
import unittest


class TestVotes(unittest.TestCase):

    def setUp(self):
        super(TestVotes, self).setUp()
        self.store = FakeStore()
        self.user = self.store.create(
            User, name="Foo Bar", email="foo@bar.com", password="whatever")

        self.votes = self.store.create(Votes, email=self.user.email)
        category = CATEGORIES[0]
        self.votes.add_vote(category.key, category.nominees[0].key)

        category = CATEGORIES[1]
        self.votes.add_vote(category.key, category.nominees[1].key)

    def test_votes(self):
        self.store.save(self.votes)
        self.assertEqual(self.votes.progress, 2.0 / len(CATEGORIES))

    def test_get_votes(self):
        self.store.save(self.votes)
        vote = self.votes.get_vote(CATEGORIES[0].key)
        self.assertEqual(vote, CATEGORIES[0].nominees[0].key)

        self.assertEqual(None, self.votes.get_vote("hardly likeley"))

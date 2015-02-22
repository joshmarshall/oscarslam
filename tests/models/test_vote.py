import unittest

from oscarslam import config
from oscarslam.categories import CATEGORIES
from oscarslam.models.user import User
from oscarslam.models.votes import Votes
from tests.helpers import FakeStore


class TestVotes(unittest.TestCase):

    def setUp(self):
        super(TestVotes, self).setUp()
        self.store = FakeStore()
        self.user = self.store.create(
            User, name="Foo Bar", email="foo@bar.com", password="whatever")

        self.votes = self.store.create(
            Votes, email=self.user.email, contest=config.CONTEST_ID)
        self.categories = CATEGORIES.contest(config.CONTEST_ID)
        category = self.categories[0]
        self.votes.add_vote(category.key, category.nominees[0].key)

        category = self.categories[1]
        self.votes.add_vote(category.key, category.nominees[1].key)

    def test_votes(self):
        self.store.save(self.votes)
        self.assertEqual(self.votes.progress, 2.0 / len(self.categories))

    def test_get_votes(self):
        self.store.save(self.votes)
        vote = self.votes.get_vote(self.categories[0].key)
        self.assertEqual(vote, self.categories[0].nominees[0].key)
        self.assertEqual(None, self.votes.get_vote("hardly likeley"))

    def test_fetch_votes(self):
        self.store.save(self.votes)
        result = self.store.fetch(
            Votes, "{0}:foo@bar.com".format(config.CONTEST_ID))
        self.assertEqual(2, len(result.votes))

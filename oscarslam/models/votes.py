from norm.model import Model
from norm.field import Field
from oscarslam.categories import CATEGORIES


class Votes(Model):

    email = Field(str, coerce=str)
    votes = Field(dict, default=dict)
    contest = Field(str, coerce=str)

    @property
    def id(self):
        return "{0}:{1}".format(self.contest, self.email)

    def __init__(self, email, contest):
        self.email = email
        self.contest = contest

    def add_vote(self, category_key, nominee_key):
        self.votes[category_key] = nominee_key

    @property
    def progress(self):
        categories = CATEGORIES.contest(self.contest)
        return float(len(self.votes)) / len(categories)

    def get_vote(self, key):
        return self.votes.get(key, None)

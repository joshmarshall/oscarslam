from norm.model import Model
from norm.field import Field
from oscarslam.categories import CATEGORIES


class Votes(Model):

    email = Field(unicode, coerce=unicode)
    votes = Field(dict, default=dict)

    @property
    def id(self):
        return self.email

    def __init__(self, email):
        self.email = email

    def add_vote(self, category_key, nominee_key):
        self.votes[category_key] = nominee_key

    @property
    def progress(self):
        return float(len(self.votes)) / len(CATEGORIES)

    def get_vote(self, key):
        return self.votes.get(key, None)

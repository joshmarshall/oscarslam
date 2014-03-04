from norm.field import Field
from norm.model import Model
from oscarslam.categories import CATEGORIES


class Winner(Model):

    winners = Field(dict, default=dict)
    contest = Field(unicode, coerce=unicode)

    @property
    def id(self):
        return self.contest

    def __init__(self, contest):
        self.contest = contest

    def add_winner(self, category, winner):
        self.winners[category] = winner

    def get_points(self, votes):
        points = 0
        for category, vote in votes.votes.items():
            if vote == self.winners.get(category):
                points += CATEGORIES.get(category).points
        return points

    def get_missed_points(self, votes):
        points = 0
        for category, vote in votes.votes.items():
            if self.winners.get(category) and \
                    vote != self.winners.get(category):
                points += CATEGORIES.get(category).points
        return points

    @property
    def remaining_points(self):
        points = 0
        for category in CATEGORIES:
            if category.key not in self.winners:
                points += category.points
        return points

    @property
    def progress(self):
        categories = 0
        for category in CATEGORIES:
            if category.key in self.winners:
                categories += 1
        return float(categories) / len(CATEGORIES)

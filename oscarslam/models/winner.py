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
        categories = CATEGORIES.contest(self.contest)
        for category, vote in votes.votes.items():
            if vote == self.winners.get(category):
                points += categories.get(category).points
        return points

    def get_missed_points(self, votes):
        points = 0
        categories = CATEGORIES.contest(self.contest)
        for category, vote in votes.votes.items():
            if self.winners.get(category) and \
                    vote != self.winners.get(category):
                points += categories.get(category).points
        return points

    @property
    def remaining_points(self):
        points = 0
        categories = CATEGORIES.contest(self.contest)
        for category in categories:
            if category.key not in self.winners:
                points += category.points
        return points

    @property
    def progress(self):
        category_count = 0
        categories = CATEGORIES.contest(self.contest)
        for category in categories:
            if category.key in self.winners:
                category_count += 1
        return float(category_count) / len(categories)

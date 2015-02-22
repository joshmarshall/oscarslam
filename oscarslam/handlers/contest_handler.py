from tornado.web import authenticated

from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.categories import CATEGORIES
from oscarslam.models.votes import Votes
from oscarslam.models.winner import Winner


class ContestHandler(BaseHandler):

    @authenticated
    def get(self, contest_id):
        categories = CATEGORIES.contest(contest_id)

        winners = self.store.fetch(Winner, contest_id)

        if not winners:
            winners = self.store.create(Winner, contest=contest_id)

        for category in categories:
            winner = self.store.fetch(Winner, category.key)
            if not winner:
                category.winner = None
            else:
                category.winner = winner.nominee

        vote_id = "{0}:{1}".format(contest_id, self.current_user.email)
        votes = self.store.fetch(Votes, vote_id)

        if not votes:
            votes = self.store.create(
                Votes, email=self.current_user.email, contest=contest_id)

        self.render(
            "contest.htm", categories=categories, votes=votes,
            winners=winners, contest_id=contest_id)

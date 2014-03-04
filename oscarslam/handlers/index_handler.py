from oscarslam import config
from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.categories import CATEGORIES
from oscarslam.models.votes import Votes
from oscarslam.models.winner import Winner


class IndexHandler(BaseHandler):

    def get(self):
        if self.current_user:
            return self._authorized_get()
        return self.render("index_unauthorized.htm")

    def _authorized_get(self):
        votes = self.store.fetch(Votes, self.current_user.email)
        categories = []

        winners = self.store.fetch(Winner, config.CONTEST_ID)
        if not winners:
            winners = self.store.create(Winner, contest=config.CONTEST_ID)

        for category in CATEGORIES:
            winner = self.store.fetch(Winner, category.key)
            if not winner:
                category.winner = None
            else:
                category.winner = winner.nominee
            categories.append(category)

        if not votes:
            votes = self.store.create(Votes, email=self.current_user.email)
        view = "index_authorized.htm"
        self.render(view, categories=CATEGORIES, votes=votes, winners=winners)

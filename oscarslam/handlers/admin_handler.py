# absolutely no tests for this...

from tornado.web import authenticated, HTTPError
from oscarslam import config
from oscarslam.categories import CATEGORIES
from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.winner import Winner


class AdminHandler(BaseHandler):

    @authenticated
    def get(self):
        self._check_admin()
        categories = CATEGORIES
        winners = self._get_winners()
        return self.render("admin.htm", categories=categories, winners=winners)

    @authenticated
    def post(self):
        self._check_admin()
        category_id = self.get_argument("category")
        nominee_id = self.get_argument("nominee")
        winners = self._get_winners()
        winners.add_winner(category_id, nominee_id)
        self.store.save(winners)
        return self.redirect("/admin")

    def _check_admin(self):
        if not self.current_user.admin:
            raise HTTPError(403, "Unauthorized.")

    def _get_winners(self):
        winners = self.store.fetch(Winner, config.CONTEST_ID)
        if not winners:
            winners = self.store.create(Winner, contest=config.CONTEST_ID)
        return winners

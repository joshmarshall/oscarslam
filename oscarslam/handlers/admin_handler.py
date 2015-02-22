# absolutely no tests for this...

from tornado.web import authenticated, HTTPError
from oscarslam.categories import CATEGORIES
from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.winner import Winner


class AdminHandler(BaseHandler):

    @property
    def queue(self):
        return self.application.settings["queue"]

    @authenticated
    def get(self, contest_id):
        self._check_admin()
        categories = CATEGORIES.contest(contest_id)
        winners = self._get_winners(contest_id)
        return self.render(
            "admin.htm", categories=categories, winners=winners,
            contest_id=contest_id)

    @authenticated
    def post(self, contest_id):
        self._check_admin()
        category_id = self.get_argument("category")
        nominee_id = self.get_argument("nominee")
        winners = self._get_winners(contest_id)
        winners.add_winner(category_id, nominee_id)
        self.store.save(winners)
        self.queue.push({
            "event": "winner",
            "category": category_id,
            "nominee": nominee_id
        })
        return self.redirect("/admin/{0}".format(contest_id))

    def _check_admin(self):
        if not self.current_user.admin:
            raise HTTPError(403, "Unauthorized.")

    def _get_winners(self, contest_id):
        winners = self.store.fetch(Winner, contest_id)
        if not winners:
            winners = self.store.create(Winner, contest=contest_id)
        return winners

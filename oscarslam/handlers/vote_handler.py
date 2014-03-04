from tornado.web import authenticated
from oscarslam import config
from oscarslam.categories import CATEGORIES
from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.votes import Votes
from oscarslam.models.winner import Winner


class VoteHandler(BaseHandler):

    @authenticated
    def get(self):
        return self.redirect("/vote/{}".format(CATEGORIES[0].key))


class VoteIdHandler(BaseHandler):

    @authenticated
    def get(self, vote_id):
        category = CATEGORIES.get(vote_id)
        votes = self._get_votes()
        return self.render(
            "vote.htm", category=category, votes=votes, vote_id=vote_id,
            categories=CATEGORIES)

    def post(self, vote_id):
        winners = self.store.fetch(Winner, config.CONTEST_ID)
        if winners and winners.winners:
            return self.redirect("/?message=contest_started")
        category = CATEGORIES.get(vote_id)
        category_index = -1
        for category in CATEGORIES:
            category_index += 1
            if category.key == vote_id:
                break

        nominee_id = self.get_argument("nominee")

        votes = self._get_votes()
        votes.add_vote(vote_id, nominee_id)
        self.store.save(votes)

        next_category_key = None

        if len(CATEGORIES) > category_index + 1:
            next_category_key = CATEGORIES[category_index + 1].key
            return self.redirect("/vote/{}".format(next_category_key))

        return self.redirect("/")

    def _get_votes(self):
        votes = self.store.fetch(Votes, self.current_user.email)
        if not votes:
            votes = self.store.create(Votes, email=self.current_user.email)
        return votes

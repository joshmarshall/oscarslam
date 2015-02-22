from tornado.web import authenticated
from oscarslam.categories import CATEGORIES
from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.votes import Votes
from oscarslam.models.winner import Winner


class VoteRedirectHandler(BaseHandler):

    def get(self, contest_id):
        categories = CATEGORIES.contest(contest_id)
        self.redirect("/contests/{}/votes/{}".format(
            contest_id, categories[0].key))


class VoteHandler(BaseHandler):

    @authenticated
    def get(self, contest_id, vote_id):
        categories = CATEGORIES.contest(contest_id)
        category = categories.get(vote_id)
        votes = self._get_votes(contest_id)
        return self.render(
            "vote.htm", category=category, votes=votes, vote_id=vote_id,
            categories=categories, contest_id=contest_id)

    def post(self, contest_id, vote_id):
        winners = self.store.fetch(Winner, contest_id)
        if winners and winners.winners:
            return self.redirect(
                "/contests/{}?message=contest_started".format(contest_id))
        categories = CATEGORIES.contest(contest_id)
        category = categories.get(vote_id)
        category_index = -1
        for category in categories:
            category_index += 1
            if category.key == vote_id:
                break

        nominee_id = self.get_argument("nominee")

        votes = self._get_votes(contest_id)
        votes.add_vote(vote_id, nominee_id)
        self.store.save(votes)

        next_category_key = None

        if len(categories) > category_index + 1:
            next_category_key = categories[category_index + 1].key
            return self.redirect(
                "/contests/{}/votes/{}".format(contest_id, next_category_key))

        return self.redirect("/")

    def _get_votes(self, contest_id):
        vote_id = "{0}:{1}".format(contest_id, self.current_user.email)
        votes = self.store.fetch(Votes, vote_id)
        if not votes:
            votes = self.store.create(
                Votes, email=self.current_user.email, contest=contest_id)
        return votes

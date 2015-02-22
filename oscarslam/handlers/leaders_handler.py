# completely untested...
from tornado.web import authenticated

from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.user import User
from oscarslam.models.winner import Winner
from oscarslam.models.votes import Votes


class LeadersHandler(BaseHandler):

    @authenticated
    def get(self, contest_id):
        leaders = []
        winners = self.store.fetch(Winner, contest_id)
        users = {user.email: user for user in self.store.find(User)}
        for votes in self.store.find(Votes, {"contest": contest_id}):
            user = users[votes.email]
            points = 0
            if votes:
                points = winners.get_points(votes)
            leaders.append((points, user))

        leaders.sort(key=lambda x: x[0], reverse=True)
        return self.render(
            "leaders.htm", leaders=leaders, contest_id=contest_id)

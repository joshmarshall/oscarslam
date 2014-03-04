# completely untested...
from tornado.web import authenticated
from oscarslam import config
from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.user import User
from oscarslam.models.winner import Winner
from oscarslam.models.votes import Votes


class LeadersHandler(BaseHandler):

    @authenticated
    def get(self):
        leaders = []
        winners = self.store.fetch(Winner, config.CONTEST_ID)
        for user in self.store.find(User):
            votes = self.store.fetch(Votes, user.email)
            points = 0
            if votes:
                points = winners.get_points(votes)
            leaders.append((points, user))

        leaders.sort(key=lambda x: x[0], reverse=True)
        return self.render("leaders.htm", leaders=leaders)

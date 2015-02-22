from oscarslam import config
from oscarslam.handlers.base_handler import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        if self.current_user:
            path = "/contests/{0}".format(config.CONTEST_ID)
            if self.request.query:
                path += "?" + self.request.query
            return self.redirect(path)
        return self.render("index.htm")

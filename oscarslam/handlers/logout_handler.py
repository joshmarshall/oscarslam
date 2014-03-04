from oscarslam.handlers.base_handler import BaseHandler


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("token")
        return self.redirect("/?message=logged_out")

from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.user import User


class SigninHandler(BaseHandler):

    def get(self):
        return self.redirect("/")

    def post(self):
        if self.current_user:
            return self.redirect("/")

        email = self.get_argument("signin-email")
        password = self.get_argument("signin-password")

        user = self.store.fetch(User, email)
        if not user:
            return self.redirect("/?message=unknown_user")

        if not user.authenticate(password):
            return self.redirect("/?message=unknown_user")

        self.set_secure_cookie("token", user.token)
        return self.redirect("/?message=welcome")

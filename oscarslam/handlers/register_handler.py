from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.user import User, Token, InvalidValue


class RegisterHandler(BaseHandler):

    def get(self):
        return self.redirect("/")

    def post(self):
        if self.current_user:
            return self.redirect("/")

        name = self.get_argument("register-name")
        email = self.get_argument("register-email")
        password = self.get_argument("register-password")

        user = self.store.fetch(User, email)
        if user:
            return self.redirect("/?message=invalid_email")

        try:
            user = self.store.create(
                User, name=name, email=email, password=password)
        except InvalidValue as exception:
            return self.redirect("/?message={}".format(exception.message))

        token = self.store.create(Token, email=user.email, token=user.token)
        self.set_secure_cookie("token", token.id)

        return self.redirect("/")

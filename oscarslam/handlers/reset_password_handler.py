from tornado import gen

from oscarslam.handlers.base_handler import BaseHandler
from oscarslam.models.user import User


class ResetPasswordHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        # if there's a signature, we'll update the password
        reset_signature = self.get_argument("reset_signature", None)
        if reset_signature:
            reset_email = self.get_argument("reset_email")
            user = self.store.fetch(User, reset_email)
            if not user or not \
                    user.verify_reset_password_url(self.request.full_url()):
                self.redirect("/?message=unknown_user")
                raise StopIteration()
            password = self.get_argument("reset-password")
            user.password = password
            self.store.save(user)
            self.redirect("/?message=password_reset")
            raise StopIteration()

        # otherwise, we are just sending the initial email
        email = self.get_argument("signin-email")

        user = self.store.fetch(User, email)
        if not user:
            self.redirect("/?message=unknown_user")

        base_url = self.request.full_url().split("?")[0]
        reset_link = user.generate_reset_password_url(base_url)

        from_email = "OscarSlam Support <support@oscarslam.com>"
        to_email = "{0} <{1}>".format(user.name, user.email)
        subject = "OSCARSLAM - Password Reset Request"
        text = self.render_string(
            "emails/reset_password.txt", user=user, reset_link=reset_link)
        html = self.render_string(
            "emails/reset_password.html", user=user, reset_link=reset_link)

        yield self.mailgun.send(
            to_email=to_email, from_email=from_email, subject=subject,
            text_message=text, html_message=html)

        self.redirect("/?message=reset_sent")
        raise StopIteration()

    def get(self):
        email = self.get_argument("reset_email")
        user = self.store.fetch(User, email)

        base_url = self.request.full_url().split("?")[0]
        reset_link = user.generate_reset_password_url(base_url)

        if not user.verify_reset_password_url(self.request.full_url()):
            return self.redirect("/?message=unknown_user")

        return self.render("reset_password.html", reset_link=reset_link)

import urllib

from oscarslam.models.user import User
from tests.helpers import HandlerTestCase


class TestResetPassword(HandlerTestCase):

    def get_signed_path(self):
        signed_url = self.user.generate_reset_password_url(
            "http://localhost:{0}/reset_password".format(self.get_http_port()))
        return signed_url.split(str(self.get_http_port()), 1)[1]

    # generating the password reset email

    def test_reset_password_post_invalid_user(self):
        body = urllib.urlencode({"signin-email": "unknown@user.com"})
        response = self.fetch("/reset_password", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assertEqual(
            "/?message=unknown_user", response.headers["Location"])

    def test_reset_password_post_with_valid_email(self):

        mailgun_results = []

        def mailgun_handler(handler):
            mailgun_results.append(handler)
            handler.finish({})

        self._mailgun_handler = mailgun_handler

        body = urllib.urlencode({"signin-email": self.user.email})

        response = self.fetch("/reset_password", body=body, method="POST")

        self.assertEqual(302, response.code)
        self.assertEqual("/?message=reset_sent", response.headers["Location"])

        self.assertTrue(len(mailgun_results) == 1)
        mailgun_request = mailgun_results[0]
        to_email = mailgun_request.get_argument("to")
        message_text = mailgun_request.get_argument("text")
        message_html = mailgun_request.get_argument("html")
        expected_base_url = "http://localhost:{0}/reset_password?".format(
            self.get_http_port())
        self.assertTrue(self.user.email in to_email)
        self.assertTrue(expected_base_url in message_text)
        self.assertTrue("href=\"" in message_html)
        self.assertTrue(expected_base_url in message_html)

    # clicking through the reset password email

    def test_get_reset_password_with_signature(self):
        signed_url = self.user.generate_reset_password_url(
            "http://localhost:{0}/reset_password".format(self.get_http_port()))
        signed_path = signed_url.split(str(self.get_http_port()), 1)[1]
        response = self.fetch(signed_path)
        self.assertEqual(200, response.code)

    def test_get_reset_password_with_invalid_signature(self):
        signed_path = self.get_signed_path()
        signed_path = signed_path.replace(
            "reset_signature=", "reset_signature=FOO")
        response = self.fetch(signed_path)
        self.assertEqual(302, response.code)
        self.assertEqual(
            "/?message=unknown_user", response.headers["Location"])

    # now for actually resetting the password

    def test_post_reset_password_updates_password(self):
        signed_path = self.get_signed_path()
        body = urllib.urlencode({"reset-password": "NEW PASSWORD"})
        response = self.fetch(signed_path, method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assertEqual(
            "/?message=password_reset", response.headers["Location"])

        user = self.store.fetch(User, self.user.email)
        self.assertTrue(user.authenticate("NEW PASSWORD"))

    def test_post_reset_password_with_invalid_signature(self):
        signed_path = self.get_signed_path()
        signed_path = signed_path.replace(
            "reset_signature=", "reset_signature=FOO")
        body = urllib.urlencode({"reset-password": "FOOBAR"})
        response = self.fetch(signed_path, method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assertEqual(
            "/?message=unknown_user", response.headers["Location"])

    def test_post_reset_password_with_unknown_user(self):
        signed_path = self.get_signed_path()
        signed_path = signed_path.replace("reset_email=", "reset_email=foo.")
        body = urllib.urlencode({"reset-password": "FOOBAR"})
        response = self.fetch(signed_path, method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assertEqual(
            "/?message=unknown_user", response.headers["Location"])

from oscarslam import config
from oscarslam.messages import MESSAGES

from tests.helpers import HandlerTestCase


class TestIndexHandler(HandlerTestCase):

    def test_index(self):
        response = self.fetch("/")
        self.assertEqual(200, response.code)

    def test_logged_in(self):
        response = self.authenticated_fetch("/?message=foo")
        self.assertEqual(302, response.code)
        self.assertEqual(
            "/contests/{0}?message=foo".format(config.CONTEST_ID),
            response.headers["Location"])

    def test_index_invalid_password(self):
        response = self.fetch("/?message=invalid_password")
        self.assertTrue(
            MESSAGES["invalid_password"]["text"] in
            response.body.decode("utf8"))

    def test_index_invalid_email(self):
        response = self.fetch("/?message=invalid_email")
        self.assertTrue(
            MESSAGES["invalid_email"]["text"] in response.body.decode("utf8"))

    def test_index_reset_sent(self):
        response = self.fetch("/?message=reset_sent")
        self.assertTrue(
            MESSAGES["reset_sent"]["text"] in response.body.decode("utf8"))

    def test_index_password_reset(self):
        response = self.fetch("/?message=password_reset")
        self.assertTrue(
            MESSAGES["password_reset"]["text"] in response.body.decode("utf8"))

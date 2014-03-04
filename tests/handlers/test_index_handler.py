from tests.helpers import HandlerTestCase
from oscarslam.messages import MESSAGES


class TestIndexHandler(HandlerTestCase):

    def test_index(self):
        response = self.fetch("/")
        self.assertEqual(200, response.code)

    def test_logged_in(self):
        response = self.authenticated_fetch("/")
        self.assertEqual(200, response.code)

    def test_index_welcome(self):
        response = self.authenticated_fetch("/?message=welcome")
        self.assertTrue("Welcome, {}.".format(self.user.name) in response.body)

    def test_index_invalid_password(self):
        response = self.authenticated_fetch("/?message=invalid_password")
        self.assertTrue(MESSAGES["invalid_password"]["text"] in response.body)

    def test_index_invalid_email(self):
        response = self.authenticated_fetch("/?message=invalid_email")
        self.assertTrue(MESSAGES["invalid_email"]["text"] in response.body)

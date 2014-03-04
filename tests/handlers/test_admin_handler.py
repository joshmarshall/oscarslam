from tests.helpers import HandlerTestCase
import urllib
from oscarslam import config
from oscarslam.categories import CATEGORIES
from oscarslam.models.user import User, Token
from oscarslam.models.winner import Winner


class TestAdminHandler(HandlerTestCase):

    def setup_admin_user(self):
        # overwriting user for authentication...
        self.user = User(name="foo", email="admin@bar.com", password="foobar")
        self.user.admin = True
        self.store.save(self.user)
        # overwriting token for cookie usage...
        self.token = self.store.create(
            Token, email=self.user.email, token=self.user.token)

    def test_admin_unauthorized(self):
        response = self.fetch("/admin")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)

        response = self.authenticated_fetch("/admin")
        self.assertEqual(403, response.code)

    def test_admin_post_unauthorized(self):
        fake_body = urllib.urlencode({
            "category": "blah",
            "nominee": "blah"
        })
        response = self.fetch("/admin", method="POST", body=fake_body)
        self.assertEqual(403, response.code)

        response = self.authenticated_fetch(
            "/admin", method="POST", body=fake_body)
        self.assertEqual(403, response.code)

    def test_admin_get(self):
        self.setup_admin_user()
        response = self.authenticated_fetch("/admin")
        self.assertEqual(200, response.code)
        # put better tests here when you're not rushing the thing...

    def test_admin_post(self):
        self.setup_admin_user()
        category_key = CATEGORIES[0].key
        nominee_key = CATEGORIES[0].nominees[0].key
        response = self.authenticated_fetch(
            "/admin", method="POST", body=urllib.urlencode({
                "category": category_key, "nominee": nominee_key
            }))
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/admin", response)
        winner = self.store.fetch(Winner, config.CONTEST_ID)
        self.assertEqual(winner.winners[category_key], nominee_key)

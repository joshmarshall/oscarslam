from tests.helpers import HandlerTestCase
from oscarslam.categories import CATEGORIES
import urllib


class TestVoteHandler(HandlerTestCase):

    def test_vote_unauthorized(self):
        response = self.fetch("/vote")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("login_required", response)

    def test_vote_authorized(self):
        response = self.authenticated_fetch("/vote")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals(
            "/vote/{}".format(CATEGORIES[0].key), response)

    def test_vote_id_unauthorized(self):
        response = self.fetch("/vote/{}".format(CATEGORIES[0].key))
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("login_required", response)

    def test_vote_id(self):
        category = CATEGORIES[0]
        response = self.authenticated_fetch(
            "/vote/{}".format(category.key))
        self.assertEqual(200, response.code)
        self.assertTrue(category.title in response.body)
        for nominee in category.nominees:
            self.assertTrue(nominee.title in response.body)
            self.assertTrue(nominee.image_url() in response.body)

    def test_vote_id_post(self):
        category = CATEGORIES[0]
        response = self.authenticated_fetch(
            "/vote/{}".format(category.key), method="POST",
            body=urllib.urlencode({
                "nominee": category.nominees[1].key
            }))
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals(
            "/vote/{}".format(CATEGORIES[1].key), response)

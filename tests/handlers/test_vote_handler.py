import urllib

from oscarslam import config
from oscarslam.categories import CATEGORIES
from tests.helpers import HandlerTestCase


class TestVoteHandler(HandlerTestCase):

    def categories(self):
        return CATEGORIES.contest(config.CONTEST_ID)

    def vote_path(self):
        return "/contests/{0}/votes".format(config.CONTEST_ID)

    def vote_category_path(self, key=None):
        key = key or self.categories()[0].key
        return self.vote_path() + "/" + key

    def test_vote_contest_redirects_to_category(self):
        response = self.fetch(self.vote_path())
        self.assert_redirected_path_equals(
            self.vote_category_path(), response)

    def test_vote_id_unauthorized(self):
        response = self.fetch(self.vote_category_path())
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("login_required", response)

    def test_vote_id(self):
        category = self.categories()[0]
        response = self.authenticated_fetch(
            self.vote_category_path(category.key))
        self.assertEqual(200, response.code)
        response_body = response.body.decode("utf8")
        self.assertTrue(category.title in response_body)
        for nominee in category.nominees:
            self.assertTrue(nominee.title in response_body)
            self.assertTrue(nominee.image_url() in response_body)

    def test_vote_id_post(self):
        category = self.categories()[0]
        response = self.authenticated_fetch(
            self.vote_category_path(category.key), method="POST",
            body=urllib.urlencode({
                "nominee": category.nominees[1].key
            }))
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals(
            self.vote_category_path(self.categories()[1].key), response)

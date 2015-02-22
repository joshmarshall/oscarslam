from oscarslam import config

from tests.helpers import HandlerTestCase


class TestContestHandler(HandlerTestCase):

    def path(self, query=""):
        return "/contests/{0}{1}".format(config.CONTEST_ID, query)

    def test_contest_redirect(self):
        response = self.fetch("/contests")
        self.assert_redirected_path_equals(self.path(), response)

    def test_contest_unauthorized(self):
        response = self.fetch(self.path())
        self.assert_redirected_path_equals("/", response)

    def test_contest_welcome(self):
        response = self.authenticated_fetch(self.path("?message=welcome"))
        self.assertTrue("Welcome, {}.".format(self.user.name) in response.body)

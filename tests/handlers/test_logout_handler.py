from tests.helpers import HandlerTestCase


class TestIndexHandler(HandlerTestCase):

    def test_logout(self):
        response = self.fetch("/logout")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("logged_out", response)
        self.assert_cookie_value("token", None, response)

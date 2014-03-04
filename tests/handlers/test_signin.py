import mock
import urllib

from tests.helpers import HandlerTestCase


class TestSignin(HandlerTestCase):

    def test_signin_get(self):
        response = self.fetch("/signin")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)

    def test_signin_authenticated_post(self):
        response = self.authenticated_fetch(
            "/signin", method="POST", body="whatever")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)

    @mock.patch("time.time")
    def test_signin_post(self, mock_time):
        mock_time.return_value = 100
        body = urllib.urlencode({
            "signin-email": self.user.email,
            "signin-password": "foobar"
        })
        response = self.fetch("/signin", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_cookie_value("token", self.user.token, response)
        self.assert_message_value("welcome", response)

    def test_signin_unknown_email(self):
        body = urllib.urlencode({
            "signin-email": "unknown@email.com",
            "signin-password": "foobar"
        })
        response = self.fetch("/signin", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("unknown_user", response)

    def test_signin_unknown_password(self):
        body = urllib.urlencode({
            "signin-email": self.user.email,
            "signin-password": "whatever"
        })
        response = self.fetch("/signin", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("unknown_user", response)

import Cookie
import mock
import urllib

from tornado.web import decode_signed_value
from tests.helpers import HandlerTestCase

from oscarslam import config
from oscarslam.models.user import User


class TestRegister(HandlerTestCase):

    def test_register_get(self):
        response = self.fetch("/register")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)

    def test_register_post_authenticated(self):
        response = self.authenticated_fetch(
            "/register", method="POST", body="foobar")
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)

    def test_invalid_name(self):
        body = urllib.urlencode({
            "register-name": "",
            "register-email": "foo2@bar.com",
            "register-password": "foobar"
        })
        response = self.fetch("/register", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("invalid_name", response)

    def test_invalid_email(self):
        body = urllib.urlencode({
            "register-name": "New User",
            "register-email": "foo",
            "register-password": "foobar"
        })
        response = self.fetch("/register", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("invalid_email", response)

    def test_invalid_password(self):
        body = urllib.urlencode({
            "register-name": "New User",
            "register-email": "foo2@bar.com",
            "register-password": "foo"
        })
        response = self.fetch("/register", method="POST", body=body)
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)
        self.assert_message_value("invalid_password", response)

    @mock.patch("time.time")
    def test_register_post(self, mock_time):
        mock_time.return_value = 100
        response = self.fetch(
            "/register", method="POST", body=urllib.urlencode({
                "register-name": "New User",
                "register-email": "new@user.com",
                "register-password": "whatever"
            }))
        self.assertEqual(302, response.code)
        self.assert_redirected_path_equals("/", response)

        user = self.store.fetch(User, "new@user.com")
        self.assertIsNotNone(user, "creates new user")
        self.assertEqual("New User", user.name)
        self.assertTrue(user.authenticate("whatever"))
        self.assertEqual("new@user.com", user.email)

        self.assertTrue("Set-Cookie" in response.headers)

        cookie = Cookie.SimpleCookie()
        cookie.load(response.headers["Set-Cookie"])

        self.assertTrue("token" in cookie)
        token_value = decode_signed_value(
            config.COOKIE_SECRET, "token", cookie["token"].value)

        self.assertEqual(user.token, token_value)

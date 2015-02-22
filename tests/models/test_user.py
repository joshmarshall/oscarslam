import hashlib
import mock
import unittest
import urllib

from tests.helpers import FakeStore

from oscarslam import config
from oscarslam.models.user import User, Token


class TestUser(unittest.TestCase):

    def setUp(self):
        super(TestUser, self).setUp()
        self.store = FakeStore()

        with mock.patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "tokenvalue"
            self.user = User.use(self.store)(
                name="Foo Bar", email="foo@bar.com", password="foobar")

    def test_user_authenticate(self):
        self.assertTrue(self.user.authenticate("foobar"))

    def test_user_admin_field(self):
        self.assertFalse(self.user.admin)
        self.user.admin = True
        self.user.store.save()
        user = self.store.fetch(User, self.user.email)
        self.assertTrue(user.admin)

    def test_user_hash_password(self):
        data = self.user.to_dict()
        self.assertFalse(data["password"] == "foobar")

    def test_user_save(self):
        self.user.store.save()
        user = User.use(self.store).store.fetch(self.user.id)
        self.assertEqual(user, self.user)
        self.assertEqual("tokenvalue", user.token)

    def test_token(self):
        token = self.store.create(
            Token, email=self.user.email, token=self.user.token)
        self.assertEqual("tokenvalue", token.id)
        self.assertEqual(self.user.email, token.email)
        self.assertEqual(self.user.token, token.id)

    @mock.patch("time.time")
    def test_generate_reset_password_url(self, mock_time):
        mock_time.return_value = 1000
        expected_signature = hashlib.sha256(
            "http://localhost/" + "foo@bar.com" + self.user.password +
            self.user.token + "4600" + config.PASSWORD_SALT).hexdigest()
        expected_url = "http://localhost/?{0}".format(urllib.urlencode({
            "reset_signature": expected_signature,
            "reset_email": self.user.email,
            "reset_expiration": 4600
        }))

        actual_url = self.user.generate_reset_password_url("http://localhost/")
        self.assertEqual(expected_url, actual_url)

    def test_verify_reset_password_url(self):
        signed_url = self.user.generate_reset_password_url("http://foo.com")
        self.assertTrue(self.user.verify_reset_password_url(signed_url))

    @mock.patch("time.time")
    def test_verify_reset_password_url_expired(self, mock_time):
        mock_time.return_value = 1000
        signed_url = self.user.generate_reset_password_url("http://foo.com")
        mock_time.return_value = 5000
        self.assertFalse(self.user.verify_reset_password_url(signed_url))

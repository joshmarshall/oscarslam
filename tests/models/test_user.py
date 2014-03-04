import mock
import unittest
from tests.helpers import FakeStore
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

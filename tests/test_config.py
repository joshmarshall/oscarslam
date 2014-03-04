import mock
import contextlib
import os
import oscarslam.config
import unittest


class TestConfig(unittest.TestCase):

    @contextlib.contextmanager
    def mock_environ(self, **parameters):
        with mock.patch.dict(os.environ, parameters):
            reload(oscarslam.config)
            yield
        reload(oscarslam.config)

    def test_defaults(self):
        self.assertEqual(8000, oscarslam.config.PORT)
        self.assertEqual("OVERWRITE", oscarslam.config.COOKIE_SECRET)
        self.assertEqual("OVERWRITE", oscarslam.config.PASSWORD_SALT)
        self.assertEqual(
            "data/nominees-2014.json", oscarslam.config.CATEGORIES_PATH)
        self.assertEqual(
            "mongodb://localhost:27017/oscarslam", oscarslam.config.DB_URI)
        self.assertFalse(oscarslam.config.DEBUG)

    def test_overwrite(self):
        with self.mock_environ(
                OSCARSLAM_PORT="9000",
                OSCARSLAM_COOKIE_SECRET="foobar",
                OSCARSLAM_PASSWORD_SALT="salted",
                OSCARSLAM_CATEGORIES_PATH="foo.json",
                # the presence of the environment variable should turn it on
                OSCARSLAM_DEBUG=""):
            self.assertEqual(9000, oscarslam.config.PORT)
            self.assertEqual("foobar", oscarslam.config.COOKIE_SECRET)
            self.assertEqual("salted", oscarslam.config.PASSWORD_SALT)
            self.assertEqual("foo.json", oscarslam.config.CATEGORIES_PATH)
            self.assertTrue(oscarslam.config.DEBUG)

    def test_overwrite_dbs(self):
        with self.mock_environ(
                OSCARSLAM_DB_URI="mongodb://foobar"):
            self.assertEqual("mongodb://foobar", oscarslam.config.DB_URI)

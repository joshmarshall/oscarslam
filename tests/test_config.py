import mock
import contextlib
import os
from oscarslam import config
import unittest


class TestConfig(unittest.TestCase):

    @contextlib.contextmanager
    def mock_environ(self, **parameters):
        with mock.patch.dict(os.environ, parameters):
            reload(config)
            yield
        reload(config)

    def test_defaults(self):
        self.assertEqual(8000, config.PORT)
        self.assertEqual("OVERWRITE", config.MAILGUN_API_URL)
        self.assertEqual("OVERWRITE", config.MAILGUN_API_KEY)
        self.assertEqual("OVERWRITE", config.COOKIE_SECRET)
        self.assertEqual("OVERWRITE", config.PASSWORD_SALT)
        self.assertEqual("OVERWRITE", config.QUEUE_URI)
        self.assertEqual(
            {"oscars2014": "data/nominees-2014.json"}, config.CONTESTS)
        self.assertEqual(
            "mongodb://localhost:27017/oscarslam", config.DB_URI)
        self.assertFalse(config.DEBUG)

    def test_overwrite(self):
        with self.mock_environ(
                OSCARSLAM_PORT="9000",
                OSCARSLAM_COOKIE_SECRET="foobar",
                OSCARSLAM_PASSWORD_SALT="salted",
                OSCARSLAM_MAILGUN_API_URL="http://foo.com",
                OSCARSLAM_MAILGUN_API_KEY="KEY",
                OSCARSLAM_CONTESTS="oscars2015,oscars2014",
                OSCARSLAM_QUEUE_URI="foo://host/queue",
                OSCARSLAM_OSCARS2015_DATA_FILE="data/2015.json",
                OSCARSLAM_OSCARS2014_DATA_FILE="data/2014.json",
                # the presence of the environment variable should turn it on
                OSCARSLAM_DEBUG=""):
            self.assertEqual(9000, config.PORT)
            self.assertEqual("foobar", config.COOKIE_SECRET)
            self.assertEqual("salted", config.PASSWORD_SALT)
            self.assertEqual("http://foo.com", config.MAILGUN_API_URL)
            self.assertEqual("foo://host/queue", config.QUEUE_URI)
            self.assertEqual("KEY", config.MAILGUN_API_KEY)
            self.assertEqual({
                "oscars2015": "data/2015.json",
                "oscars2014": "data/2014.json"
            }, config.CONTESTS)
            self.assertEqual("oscars2015", config.CONTEST_ID)
            self.assertTrue(config.DEBUG)

    def test_overwrite_dbs(self):
        with self.mock_environ(
                OSCARSLAM_DB_URI="mongodb://foobar"):
            self.assertEqual("mongodb://foobar", config.DB_URI)

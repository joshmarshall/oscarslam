import mock
import contextlib
import os
from oscarslam import config
import shutil
import tempfile
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
        self.assertEqual({
            "oscars2014": "data/oscars2014.json",
            "oscars2015": "data/oscars2015.json",
            "oscars2016": "data/oscars2016.json",
        }, config.CONTESTS)
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
                OSCARSLAM_QUEUE_URI="foo://u:p@host/queue",
                # the presence of the environment variable should turn it on
                OSCARSLAM_DEBUG=""):
            self.assertEqual(9000, config.PORT)
            self.assertEqual("foobar", config.COOKIE_SECRET)
            self.assertEqual("salted", config.PASSWORD_SALT)
            self.assertEqual("http://foo.com", config.MAILGUN_API_URL)
            self.assertEqual("https://host", config.QUEUE.identity_url)
            self.assertEqual("queue", config.QUEUE.queue)
            self.assertEqual("KEY", config.MAILGUN_API_KEY)
            self.assertEqual("oscars2016", config.CONTEST_ID)
            self.assertTrue(config.DEBUG)

    def test_overwrite_contests(self):
        tempdir = tempfile.mkdtemp()
        try:
            path = os.path.join(tempdir, "contest.json")
            with open(path, "wb") as fp:
                fp.write("CONTENT")
            with self.mock_environ(OSCARSLAM_DATA_FOLDER=tempdir):
                self.assertEqual({"contest": path}, config.CONTESTS)
        finally:
            shutil.rmtree(tempdir)

    def test_overwrite_dbs(self):
        with self.mock_environ(
                OSCARSLAM_DB_URI="mongodb://foobar"):
            self.assertEqual("mongodb://foobar", config.DB_URI)

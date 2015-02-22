import Cookie
import tempfile
from tornado.testing import bind_unused_port
from tornado.web import decode_signed_value
import urlparse

import mock
import norm.framework
from norm.backends.dbm_backend import DBMConnection
from testnado.handler_test_case import HandlerTestCase as TNHandlerTestCase
from testnado.credentials.cookie_credentials import CookieCredentials

from oscarslam import config
from oscarslam.application import Application
from oscarslam.mailgun_client import MailGunClient
from oscarslam.models.user import User, Token


class HandlerTestCase(TNHandlerTestCase):

    def setUp(self):
        super(HandlerTestCase, self).setUp()
        self.cookie_secret = config.COOKIE_SECRET
        self.mailgun_app = mock_mailgun(
            self.io_loop, self.mailgun_handler)
        self.mailgun_app.listen(self.mailgun_port, io_loop=self.io_loop)
        self.user = self.store.create(
            User, name="Foo Bar", email="foo@bar.com", password="foobar")
        self.token = self.store.create(
            Token, email=self.user.email, token=self.user.token)

    def tearDown(self):
        super(HandlerTestCase, self).tearDown()
        # should delete everything...
        self.dbfile.close()

    def mailgun_handler(self, handler):
        if not hasattr(self, "_mailgun_handler"):
            raise Exception("Not implemented.")
        return self._mailgun_handler(handler)

    def get_app(self):
        self.dbfile = tempfile.NamedTemporaryFile(suffix=".db")
        self.dburi = "dbm://{}".format(self.dbfile.name)
        self.connection = DBMConnection.from_uri(self.dburi)
        self.store = self.connection.get_store()
        _, self.mailgun_port = bind_unused_port()
        self.mailgun_url = "http://localhost:{0}/v2/account".format(
            self.mailgun_port)
        mailgun = MailGunClient(self.mailgun_url, "KEY", self.io_loop)
        queue = mock.Mock()
        return Application(store=self.store, mailgun=mailgun, queue=queue)

    def get_credentials(self):
        return CookieCredentials("token", self.token.id, self.cookie_secret)

    def assert_cookie_value(self, name, value, response):
        self.assertTrue("Set-Cookie" in response.headers)
        cookie = Cookie.SimpleCookie(response.headers["Set-Cookie"])
        self.assertTrue(name in cookie, "expected {} cookie".format(name))
        actual_value = decode_signed_value(
            config.COOKIE_SECRET, name, cookie[name].value)
        self.assertEqual(value, actual_value)

    def assert_message_value(self, value, response):
        parsed = urlparse.urlparse(response.headers["Location"])
        query_arguments = dict([
            (k, v[0]) for k, v in urlparse.parse_qs(parsed.query).items()
        ])
        self.assertTrue("message" in query_arguments)
        self.assertEqual(value, query_arguments["message"])


@norm.framework.store
class FakeStore(object):

    def __init__(self):
        self._data = {}

    @norm.framework.serialize
    def save(self, instance):
        model_name = instance.__class__.__name__
        instance_data = instance.to_dict()
        instance_id = "{}.{}".format(model_name, instance.identify())
        self._data[instance_id] = instance_data

    @norm.framework.deserialize
    def fetch(self, model, model_id):
        full_id = "{}.{}".format(model.__name__, model_id)
        return model.from_dict(self._data[full_id])

    @norm.framework.deserialize
    def first(self, model):
        match = "{}.".format(model.__name__)
        for key in self._data:
            if key.startswith(match):
                return model.from_dict(self._data[key])

    @norm.framework.deserialize
    def create(self, model, **kwargs):
        instance = model(**kwargs)
        self.save(instance)
        return instance


from tornado.web import RequestHandler, Application as TornadoApplication


class MessagesHandler(RequestHandler):

    def post(self):
        return self.application.settings["handle"](self)


def mock_mailgun(ioloop, handler):
    application = TornadoApplication([
        ("/v2/account/messages", MessagesHandler)
    ], handle=handler)
    return application

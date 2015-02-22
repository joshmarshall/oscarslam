# Simple, Tornado IOLoop-based MailGun integration

from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application

from tests.helpers import MessagesHandler
from oscarslam.mailgun_client import MailGunClient, MailGunError


class TestMailGun(AsyncHTTPTestCase):

    def setUp(self):
        super(TestMailGun, self).setUp()

        def default_handle(handler):
            raise Exception("Not implemented.")

        self._handle_message = default_handle

    def get_app(self):
        return Application([
            ("/v2/account/messages", MessagesHandler)
        ], handle=self.handle_message)

    def handle_message(self, handler):
        return self._handle_message(handler)

    @gen_test
    def test_mailgun_api_successful(self):

        from_email = "Joe User <joe@user.com>"
        to_email = "Jane Sender <jane@sender.com>"
        subject = "Message Subject"
        text_message = "This is plain text message."
        html_message = "<html>This is <b>HTML!</b></html>"

        def handle(handler):
            assert handler.get_argument("from") == from_email
            assert handler.get_argument("to") == to_email
            assert handler.get_argument("subject") == subject
            assert handler.get_argument("text") == text_message
            assert handler.get_argument("html") == html_message
            return handler.finish({
                "message": "Queued.",
                "id": "AWESOME ID"
            })

        self._handle_message = handle

        base_url = "http://localhost:{0}/v2/account".format(
            self.get_http_port())
        api_key = "API_KEY"
        client = MailGunClient(base_url, api_key, ioloop=self.io_loop)

        yield client.send(
            from_email=from_email, to_email=to_email, subject=subject,
            text_message=text_message, html_message=html_message)

        self.assertTrue(True, "We didn't fail. Good job.")

    @gen_test
    def test_mailgun_api_send_with_failure(self):
        base_url = "http://localhost:{0}/v2/account".format(
            self.get_http_port())
        api_key = "API_KEY"
        client = MailGunClient(base_url, api_key, ioloop=self.io_loop)

        with self.assertRaises(MailGunError):
            yield client.send(
                from_email="from@user.com", to_email="to@you.com",
                subject="Subject", text_message="Text", html_message="HTML")

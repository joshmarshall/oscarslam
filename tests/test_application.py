import mock
from testnado.handler_test_case import HandlerTestCase
from oscarslam.application import Application


class TestApplication(HandlerTestCase):

    def get_app(self):
        store = mock.Mock()
        mailgun = mock.Mock()
        queue = mock.Mock()
        return Application(store=store, mailgun=mailgun, queue=queue)

    def test_index(self):
        response = self.fetch("/")
        self.assertEqual(200, response.code)

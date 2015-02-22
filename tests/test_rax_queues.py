import json

from tornado.testing import AsyncTestCase, gen_test
from tornadomock.service_case_helpers import ServiceCaseHelpers

from oscarslam.rax_queue import RaxQueue
from tests.samples import RAX_AUTH_DATA


class TestRaxQueue(ServiceCaseHelpers, AsyncTestCase):

    def setUp(self):
        super(TestRaxQueue, self).setUp()

        def id_handle(handler):
            self.identity_requests.append(handler.request)
            auth_data = json.dumps(RAX_AUTH_DATA)
            auth_data = auth_data.replace(
                "{{QUEUE_URL}}", self.queue_service.base_url)
            handler.finish(auth_data)

        self.identity_service = self.add_service()
        self.identity_service.add_method("POST", "/v2.0/tokens", id_handle)

        def health_handle(handler):
            handler.set_status(204)

        def get_message_handle(handler):
            self.get_message_requests.append(handler.request)
            base_url = handler.request.full_url().split("?")[0]
            next_url = base_url + "?marker=" + str(
                len(self.get_message_requests))
            handler.write({
                "links": [{"rel": "next", "href": next_url}],
                "messages": [{"ttl": 10, "age": 10, "body": {"event": "foo"}}]
            })

        def post_message_handle(handler):
            self.post_message_requests.append(handler.request)
            handler.set_status(201)
            handler.finish({
                "resources": [
                    "/v1/queues/myqueue/messages/1",
                ]
            })

        self.identity_requests = []
        self.get_message_requests = []
        self.post_message_requests = []

        self.queue_service = self.add_service()
        self.queue_service.add_method("GET", "/v1/health", health_handle)
        self.queue_service.add_method(
            "GET", "/v1/queues/myqueue/messages", get_message_handle)
        self.queue_service.add_method(
            "POST", "/v1/queues/myqueue/messages", post_message_handle)

        queue_uri = "raxqueue://user:key@{}/myqueue".format(
            self.identity_service.host)

        self.client = RaxQueue(queue_uri, self.io_loop)

    @gen_test
    def test_connect(self):
        self.start_services()

        yield self.client.connect()
        self.assertEqual(1, len(self.identity_requests))
        request = self.identity_requests[0]
        self.assertEqual("application/json", request.headers["Content-type"])
        body = json.loads(request.body)
        credentials = body["auth"]["RAX-KSKEY:apiKeyCredentials"]
        self.assertEqual(credentials["username"], "user")
        self.assertEqual(credentials["apiKey"], "key")

    @gen_test
    def test_fetch_messages(self):
        self.start_services()

        result = yield self.client.connect()
        self.assertEqual({"status": "success"}, result)
        result = yield self.client.fetch_messages()
        self.assertEqual("success", result["status"])
        messages = result["messages"]
        self.assertEqual(1, len(messages))
        self.assertEqual({"event": "foo"}, messages[0]["body"])
        self.queue_service.assert_requested(
            "GET", "/v1/queues/myqueue/messages", headers={
                "X-Auth-Token": "TOKEN",
                "Client-Id": self.client.receive_client_id})

    @gen_test
    def test_push_messages(self):
        self.start_services()
        yield self.client.connect()

        message = {"event": "foo"}
        result = yield self.client.push_message(message, ttl=60)
        self.assertEqual("success", result["status"])
        self.assertTrue("resource" in result)

        self.queue_service.assert_requested(
            "POST", "/v1/queues/myqueue/messages", headers={
                "X-Auth-Token": "TOKEN",
                "Client-Id": self.client.send_client_id})

        request = self.post_message_requests[0]
        request = json.loads(request.body)
        self.assertEqual([{"ttl": 60, "body": message}], request)

import json
import uuid
import urlparse

from tornado import gen
from tornado.httpclient import AsyncHTTPClient


class RaxQueue(object):

    def __init__(self, queue_uri, ioloop):
        self.queue_uri = queue_uri
        parsed_uri = urlparse.urlparse(queue_uri)
        auth, self.identity_host = parsed_uri.netloc.split("@")
        self.ioloop = ioloop
        self.protocol = "https" if parsed_uri.scheme == "raxqueues" else "http"
        self.identity_url = "{}://{}/v2.0/tokens".format(
            self.protocol, self.identity_host)
        self.queue = parsed_uri.path[1:]
        self.username, self.api_key = auth.split(":")
        self.client = AsyncHTTPClient(io_loop=self.ioloop)
        self.receive_client_id = uuid.uuid4().hex
        self.send_client_id = uuid.uuid4().hex
        self.next_url = None

    @gen.coroutine
    def connect(self):
        auth_body = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials": {
                    "username": self.username,
                    "apiKey": self.api_key
                }
            }
        }
        response = yield self.client.fetch(
            self.identity_url, method="POST", body=json.dumps(auth_body),
            headers={"Content-type": "application/json"},
            raise_error=False)

        if response.code != 200:
            raise gen.Return({"status": "failed", "code": response.code})

        auth_response = json.loads(response.body)
        self.token = auth_response["access"]["token"]["id"]
        self.region = \
            auth_response["access"]["user"]["RAX-AUTH:defaultRegion"]
        self.token_expires = auth_response["access"]["token"]["expires"]
        for service in auth_response["access"]["serviceCatalog"]:
            if service["type"] != "rax:queues":
                continue
            for endpoint in service["endpoints"]:
                if endpoint["region"] != self.region:
                    continue
                self.queue_base_url = endpoint["publicURL"]

        raise gen.Return({"status": "success"})

    @gen.coroutine
    def fetch_messages(self):
        if not self.next_url:
            self.next_url = "{}/queues/{}/messages".format(
                self.queue_base_url, self.queue)

        response = yield self.client.fetch(
            self.next_url, headers={
                "X-Auth-Token": self.token,
                "Client-Id": self.receive_client_id
            }, raise_error=False)

        if response.code > 399:
            raise gen.Return({
                "status": "error",
                "code": response.code,
                "body": response.body
            })

        if response.code == 204:
            raise gen.Return({
                "status": "success",
                "messages": []
            })

        body = json.loads(response.body)
        next_urls = [l["href"] for l in body["links"] if l["rel"] == "next"]
        self.next_url = urlparse.urljoin(self.queue_base_url, next_urls[0])
        messages = [m for m in body["messages"]]
        raise gen.Return({
            "status": "success",
            "messages": messages
        })

    @gen.coroutine
    def push_message(self, message, ttl):
        messages_url = "{}/queues/{}/messages".format(
            self.queue_base_url, self.queue)
        body = json.dumps([{"ttl": ttl, "body": message}])
        response = yield self.client.fetch(
            messages_url, method="POST", body=body, headers={
                "X-Auth-Token": self.token,
                "Client-Id": self.send_client_id}, raise_error=False)

        if response.code != 201:
            logging.error("Failed to push message: {} {}".format(
                response.code, response.body))
            raise gen.Return({
                "status": "failed",
                "code": response.code,
                "body": response.body
            })

        body = json.loads(response.body)
        raise gen.Return({
            "status": "success",
            "resource": body["resources"][0]
        })

# simple, IOLoop-based Mailgun client.

import urllib.parse

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError


class MailGunClient(object):

    def __init__(self, base_url, api_key, ioloop):
        self.base_url = base_url
        self.api_key = api_key
        self.ioloop = ioloop

    @gen.coroutine
    def send(self, to_email, from_email, subject, text_message, html_message):
        url = "{0}/messages".format(self.base_url)
        client = AsyncHTTPClient()
        body = urllib.parse.urlencode({
            "to": to_email,
            "from": from_email,
            "subject": subject,
            "text": text_message,
            "html": html_message
        })
        request = HTTPRequest(
            url, method="POST", auth_username="api",
            auth_password=self.api_key, body=body)
        try:
            yield client.fetch(request)
        except HTTPError as exception:
            raise MailGunError(
                "Error communicating with MailGun: ({0}) {1}".format(
                    exception.code, exception.message))


class MailGunError(Exception):
    pass

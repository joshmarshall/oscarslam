import logging

import tornado.log
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.netutil import bind_sockets
from tornadorax.identity_client import IdentityClient
from norm.backends.dbm_backend import DBMConnection

from oscarslam import config
from oscarslam.application import Application
from oscarslam.event_queue import EventQueue
from oscarslam.mailgun_client import MailGunClient
from oscarslam.models.mongodb_backend import MongoDBConnection


CONNECTIONS = {
    "mongodb": MongoDBConnection,
    "dbm": DBMConnection
}


def wait_for_future(f):
    ioloop = IOLoop.current()
    f.add_done_callback(lambda _: ioloop.stop())
    ioloop.start()
    return f.result()


def get_rax_queue(ioloop):
    client = IdentityClient(
        config.QUEUE.identity_url, config.QUEUE.credentials, ioloop)
    wait_for_future(client.authorize())
    queue_service = client.build_service("rax:queues")
    queue = wait_for_future(queue_service.fetch_queue(config.QUEUE.queue))
    return EventQueue(queue, ioloop)


def main():
    tornado.log.enable_pretty_logging()
    logging.getLogger().setLevel(config.LOG_LEVEL)

    logging.info("Listening on: {0}".format(config.PORT))
    sockets = bind_sockets(config.PORT)
    tornado.process.fork_processes(config.PROCESSES)

    ioloop = IOLoop.current()

    protocol = config.DB_URI.split("://")[0]
    connection = CONNECTIONS[protocol].from_uri(config.DB_URI)
    store = connection.get_store()

    queue = get_rax_queue(ioloop)

    mailgun = MailGunClient(
        config.MAILGUN_API_URL, config.MAILGUN_API_KEY, ioloop)

    application = Application(store=store, mailgun=mailgun, queue=queue)
    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)

    ioloop.start()


if __name__ == "__main__":
    main()

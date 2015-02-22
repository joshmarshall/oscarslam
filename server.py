from tornado.ioloop import IOLoop
from norm.backends.dbm_backend import DBMConnection

from oscarslam import config
from oscarslam.application import Application
from oscarslam.event_queue import EventQueue
from oscarslam.mailgun_client import MailGunClient
from oscarslam.models.mongodb_backend import MongoDBConnection
from oscarslam.rax_queue import RaxQueue


CONNECTIONS = {
    "mongodb": MongoDBConnection,
    "dbm": DBMConnection
}


def main():
    ioloop = IOLoop.instance()
    protocol = config.DB_URI.split("://")[0]
    connection = CONNECTIONS[protocol].from_uri(config.DB_URI)
    store = connection.get_store()
    rax_queue = RaxQueue(config.QUEUE_URI, ioloop)
    queue = EventQueue(rax_queue, ioloop)
    mailgun = MailGunClient(
        config.MAILGUN_API_URL, config.MAILGUN_API_KEY, ioloop)
    application = Application(store=store, mailgun=mailgun, queue=queue)
    application.listen(config.PORT)
    print "Listening on {}".format(config.PORT)
    ioloop.start()


if __name__ == "__main__":
    main()

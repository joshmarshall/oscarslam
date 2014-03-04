from oscarslam import config
from oscarslam.application import Application
from tornado.ioloop import IOLoop
from norm.backends.dbm_backend import DBMConnection
from norm.backends.mongodb_backend import MongoDBConnection


CONNECTIONS = {
    "mongodb": MongoDBConnection,
    "dbm": DBMConnection
}


def main():
    protocol = config.DB_URI.split("://")[0]
    connection = CONNECTIONS[protocol].from_uri(config.DB_URI)
    store = connection.get_store()
    application = Application(store=store)
    application.listen(config.PORT)
    print "Listening on {}".format(config.PORT)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()

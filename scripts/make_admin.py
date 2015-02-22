import os
import sys

_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, _PATH)

from norm.backends.dbm_backend import DBMConnection

from oscarslam import config
from oscarslam.models.mongodb_backend import MongoDBConnection
from oscarslam.models.user import User


CONNECTIONS = {
    "mongodb": MongoDBConnection,
    "dbm": DBMConnection
}


def main():
    email = sys.argv[1]

    protocol = config.DB_URI.split("://")[0]
    connection = CONNECTIONS[protocol].from_uri(config.DB_URI)
    store = connection.get_store()

    user = store.fetch(User, email)
    if not user:
        raise Exception("Unknown user: {}".format(email))

    print "Making user '{}' an admin.".format(user.name)
    user.admin = True
    store.save(user)


if __name__ == "__main__":
    main()

# make this a real migrations thing later.
import os
import pymongo
import sys
import urlparse

_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, _PATH)

from oscarslam import config


def main():
    database_name = urlparse.urlparse(config.DB_URI).path[1:]
    connection = pymongo.MongoClient(config.DB_URI)
    database = connection[database_name]

    for votes in database.votes.find():
        if "contest" not in votes:
            print "Migrating the following record: "
            print votes
            print ""
            original_id = votes["_id"]
            contest_id = "{0}:{1}".format("oscars2014", votes["email"])
            votes["_id"] = contest_id
            votes["contest"] = "oscars2014"
            database.votes.save(votes, safe=True)
            print "Removing old record."
            database.votes.remove({"_id": original_id})
            print ""

    for votes in database.votes.find():
        print votes


if __name__ == "__main__":
    main()

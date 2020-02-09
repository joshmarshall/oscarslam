import collections
import glob
import os
import urllib.parse as urlparse


_PREFIX = "OSCARSLAM"
_QUEUE = collections.namedtuple(
    "Queue", ["credentials", "identity_url", "queue"])


def _default(environ_name, default_value, cast=lambda x: x):
    environ_name = "{}_{}".format(_PREFIX, environ_name)
    return cast(os.environ.get(environ_name, default_value))


def _queue_uri(queue_uri):
    parsed_uri = urlparse.urlparse(queue_uri)
    raw_credentials, domain = parsed_uri.netloc.split("@")
    username, key = raw_credentials.split(":")
    identity_url = "https://{0}".format(domain)
    credentials = {
        "RAX-KSKEY:apiKeyCredentials": {
            "username": username,
            "apiKey": key
        }
    }
    queue_name = parsed_uri.path[1:]
    return _QUEUE(credentials, identity_url, queue_name)


def _populate_contests(folder):
    contests = {}
    for json_file in glob.glob(os.path.join(folder, "*.json")):
        contest_name, _ = os.path.splitext(os.path.basename(json_file))
        contests[contest_name] = json_file
    return contests


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

PORT = _default("PORT", 8000, int)
PROCESSES = _default("PROCESSES", 0, int)
COOKIE_SECRET = _default("COOKIE_SECRET", "OVERWRITE")
STATIC_FOLDER = _default("STATIC_FOLDER", os.path.join(BASE_DIR, "static"))
VIEW_FOLDER = _default("VIEW_FOLDER", os.path.join(BASE_DIR, "views"))
PASSWORD_SALT = _default("PASSWORD_SALT", "OVERWRITE")
MAILGUN_API_URL = _default("MAILGUN_API_URL", "OVERWRITE")
MAILGUN_API_KEY = _default("MAILGUN_API_KEY", "OVERWRITE")
QUEUE = _queue_uri((_default("QUEUE_URI", "raxqueue://u:p@i/q")))
DB_URI = _default("DB_URI", "mongodb://localhost:27017/oscarslam")
DEBUG = _default("DEBUG", False, cast=lambda x: x is not False)
LOG_LEVEL = _default("LOG_LEVEL", "DEBUG")
DATA_FOLDER = _default("DATA_FOLDER", "data")

CONTESTS = _populate_contests(DATA_FOLDER)

# default contest id
_DEFAULT_CONTEST = sorted(CONTESTS.keys())[-1]
CONTEST_ID = _default("CURRENT_CONTEST", _DEFAULT_CONTEST)

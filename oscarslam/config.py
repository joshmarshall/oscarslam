import os


_PREFIX = "OSCARSLAM"


def _default(environ_name, default_value, cast=lambda x: x):
    environ_name = "{}_{}".format(_PREFIX, environ_name)
    return cast(os.environ.get(environ_name, default_value))


PORT = _default("PORT", 8000, int)
COOKIE_SECRET = _default("COOKIE_SECRET", "OVERWRITE")
PASSWORD_SALT = _default("PASSWORD_SALT", "OVERWRITE")
MAILGUN_API_URL = _default("MAILGUN_API_URL", "OVERWRITE")
MAILGUN_API_KEY = _default("MAILGUN_API_KEY", "OVERWRITE")
QUEUE_URI = _default("QUEUE_URI", "OVERWRITE")
DB_URI = _default("DB_URI", "mongodb://localhost:27017/oscarslam")
DEBUG = _default("DEBUG", False, cast=lambda x: x is not False)
CONTESTS = {}


_CONTEST_KEYS = _default("CONTESTS", "oscars2014").split(",")

for key in _CONTEST_KEYS:
    data_file = os.environ.get("OSCARSLAM_{0}_DATA_FILE".format(key.upper()))
    if data_file:
        CONTESTS[key] = data_file

# for now, at least
CONTESTS.setdefault("oscars2014", "data/nominees-2014.json")

# default contest id
CONTEST_ID = _CONTEST_KEYS[0]

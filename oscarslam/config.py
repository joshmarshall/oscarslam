import os


_PREFIX = "OSCARSLAM"


def _default(environ_name, default_value, cast=lambda x: x):
    environ_name = "{}_{}".format(_PREFIX, environ_name)
    return cast(os.environ.get(environ_name, default_value))


PORT = _default("PORT", 8000, int)
COOKIE_SECRET = _default("COOKIE_SECRET", "OVERWRITE")
PASSWORD_SALT = _default("PASSWORD_SALT", "OVERWRITE")
DB_URI = _default("DB_URI", "mongodb://localhost:27017/oscarslam")
CATEGORIES_PATH = _default("CATEGORIES_PATH", "data/nominees-2014.json")
DEBUG = _default("DEBUG", False, cast=lambda x: x is not False)
CONTEST_ID = "oscars2014"

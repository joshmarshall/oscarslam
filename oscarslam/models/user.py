import hashlib
import re
import time
import urllib
import urllib.parse as urlparse
import uuid

from norm.field import Field
from norm.model import Model

from oscarslam import config

# an hour is plenty. read your email.
_RESET_EXPIRATION = 3600


def hash_password(_, password):
    if len(password) < 6:
        raise InvalidValue("invalid_password")
    new_password = "{}{}".format(config.PASSWORD_SALT, password)
    return hashlib.sha512(new_password.encode("utf8")).hexdigest()


def validate_name(_, name):
    if len(name) < 3:
        raise InvalidValue("invalid_name")
    return name


def validate_email(_, email):
    email = email.lower()
    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,10}$", email):
        raise InvalidValue("invalid_email")
    return email


def generate_token():
    return uuid.uuid4().hex


class User(Model):

    name = Field(str, coerce=str, serialize=validate_name)
    email = Field(str, coerce=str, serialize=validate_email)
    password = Field(str, coerce=str, serialize=hash_password)
    token = Field(str, coerce=str, default=generate_token)
    admin = Field(bool, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @property
    def id(self):
        return self.email

    def generate_reset_password_url(self, base_url, expiration=None):
        expiration = str(int(expiration or time.time() + _RESET_EXPIRATION))
        raw_value = base_url + self.email + self.password + self.token + \
            expiration + config.PASSWORD_SALT
        signature = hashlib.sha256(raw_value.encode("utf8")).hexdigest()

        # won't be friendly with query parameters.
        url = "{0}?{1}".format(base_url, urllib.parse.urlencode({
            "reset_signature": signature,
            "reset_expiration": expiration,
            "reset_email": self.email
        }))
        return url

    def verify_reset_password_url(self, signed_url):
        base_url, query_arguments = signed_url.split("?")
        query_parameters = dict([
            (k, v) for k, v in urlparse.parse_qsl(query_arguments)
        ])
        expiration = query_parameters["reset_expiration"]
        if int(expiration) < time.time():
            return False
        generated_url = self.generate_reset_password_url(base_url, expiration)
        return signed_url == generated_url

    def authenticate(self, password):
        return self.password == hash_password(self, password)


class Token(Model):

    token = Field(str, coerce=str)
    email = Field(str, coerce=str)

    def __init__(self, email, token):
        self.email = email
        self.token = token

    @property
    def id(self):
        return self.token


class InvalidValue(Exception):

    def __init__(self, message):
        self.message = message

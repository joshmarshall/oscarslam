import hashlib
import re
import string
import uuid

from norm.field import Field
from norm.model import Model

from oscarslam import config


_LETTERS = "".join(string.letters + string.digits)


def hash_password(password):
    if len(password) < 6:
        raise InvalidValue("invalid_password")
    new_password = "{}{}".format(config.PASSWORD_SALT, password)
    return hashlib.sha512(new_password).hexdigest()


def validate_name(name):
    if len(name) < 3:
        raise InvalidValue("invalid_name")
    return name


def validate_email(email):
    email = email.lower()
    if not re.match("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,10}$", email):
        raise InvalidValue("invalid_email")
    return email


def generate_token():
    return uuid.uuid4().hex


class User(Model):

    name = Field(unicode, coerce=unicode, serialize=validate_name)
    email = Field(unicode, coerce=unicode, serialize=validate_email)
    password = Field(unicode, coerce=unicode, serialize=hash_password)
    token = Field(unicode, coerce=unicode, default=generate_token)
    admin = Field(bool, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @property
    def id(self):
        return self.email

    def authenticate(self, password):
        return self.password == hash_password(password)


class Token(Model):

    token = Field(unicode, coerce=unicode)
    email = Field(unicode, coerce=unicode)

    def __init__(self, email, token):
        self.email = email
        self.token = token

    @property
    def id(self):
        return self.token


class InvalidValue(Exception):

    def __init__(self, message):
        self.message = message

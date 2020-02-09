#!/usr/bin/env python

from datetime import datetime
from setuptools import setup, find_packages
from subprocess import check_output

_LAST_TIME = check_output(
    "git log --pretty=format:%ct -n 1", shell=True).decode("utf8")
_LAST_HASH = check_output(
    "git log --pretty=format:%h -n 1", shell=True).decode("utf8")
_CURRENT_VERSION = datetime.fromtimestamp(
    int(_LAST_TIME)).strftime("%Y.%m%d") + "-" + _LAST_HASH

with open("requirements.txt") as rfp:
    install_requires = [r.strip() for r in rfp.readlines()]


setup(
    name="oscarslam",
    version=_CURRENT_VERSION,
    description="Oscar Competition",
    author="Josh Marshall",
    author_email="catchjosh@gmail.com",
    packages=find_packages(exclude=["tests", "dist"]),
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["oscarslam = oscarslam.service:main"],
    })

#!/usr/bin/env python
# coding=utf-8
"""Setup script."""

import sys
from setuptools import setup, find_packages

dependencies = [
    "WTForms",
    "pyotp",
    "jinja2",
    "qrcode"
]
name = "WTF-OTP"
desc = "One-Time Password for WTForms"

if sys.version_info < (2, 7):
    raise RuntimeError(
        "Not supported on python that is older then version 2.7."
    )

try:
    with open('README.md') as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

with open('VERSION') as version_in:
    version = version_in.read()

setup(
    name=name,
    version=version,
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=dependencies,
    zip_safe=False,
    author="Hiroaki Yamamoto",
    author_email="hiroaki@hysoftware.net",
    license="MIT",
    keywords="WTForms WT-Forms OTP One Time Password",
    url="https://github.com/hiroaki-yamamoto/WTF-OTP",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        ("Topic :: Internet :: WWW/HTTP :: "
         "Dynamic Content :: CGI Tools/Libraries"),
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Flask"
    ]
)

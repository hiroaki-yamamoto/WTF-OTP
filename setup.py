#!/usr/bin/env python
# coding=utf-8
"""Setup script."""

import sys
from setuptools import setup, find_packages

dependencies = [
    "WTForms==2.1"
]
name = "WTF-OTP"
desc = "One-Time Password for WTForms"
version = "0.0.0"

if sys.version_info < (2, 7):
    raise RuntimeError("Not supported on earlier then python 2.7.")

try:
    with open('README.rst') as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

setup(
    name=name,
    version=version,
    description=desc,
    long_description=long_desc,
    packages=find_packages(exclude=["tests"]),
    install_requires=dependencies,
    zip_safe=False,
    author="Hiroaki Yamamoto",
    author_email="hiroaki@hysoftware.net",
    license="MIT",
    keywords="WTForms WT-Forms OTP One Time Password",
    url="https://github.com/hiroaki-yamamoto/mongoengine-goodjson",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5"
    ]
)

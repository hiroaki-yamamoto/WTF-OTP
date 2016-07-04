#!/usr/bin/env python
# coding=utf-8

"""SecretKeyField module."""

from wtforms.fields import Field

from ..widgets import OTPSecretKeyWidget
from pyotp import random_base32


class OTPSecretKeyField(Field):
    """
    OTPSecretKeyField.

    This field is used for generating secret key. Note that the secret key
    is generated on client-side. Therefore, but I think the same thing happens
    on server-side, the secret key transaction should be secured. i.e. it
    should be protected with SSL for example.
    """

    widget = OTPSecretKeyWidget()

    def generate(self, **kwargs):
        """
        Generate Secret Key.

        Parameters:
            **kwargs: Optional. Any keyword arguments to be passed to
            `pyotp.random_base32`.

        Return Value: 16 chars random string that is able to be a secret key.
        """
        return random_base32(**kwargs)

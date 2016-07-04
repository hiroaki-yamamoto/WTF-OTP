#!/usr/bin/env python
# coding=utf-8

"""SecretKeyField module."""

import random
from wtforms.fields import Field

from ..widgets import OTPSecretKeyWidget


class OTPSecretKeyField(Field):
    """
    OTPSecretKeyField.

    This field is used for generating secret key. Note that the secret key
    is generated on client-side. Therefore, but I think the same thing happens
    on server-side, the secret key transaction should be secured. i.e. it
    should be protected with SSL for example.
    """

    widget = OTPSecretKeyWidget()

    def generate(self):
        """
        Generate Secret Key.

        Return Value: 16 chars random string that is able to be a secret key.
        """
        return ("").join([random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        ) for unused in range(16)])

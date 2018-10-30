#!/usr/bin/env python
# coding=utf-8

"""SecretKeyField module."""

from io import BytesIO

from wtforms.fields import StringField
from pyotp import random_base32
from pyotp.utils import build_uri as build_otp_uri
from qrcode import make as generate_qrcode
from qrcode.image.svg import SvgPathImage as svg

from ..widgets import OTPSecretKeyWidget


class OTPSecretKeyField(StringField):
    """
    OTPSecretKeyField.

    This field is used for generating secret key. Note that the secret key
    is generated on client-side. Therefore, but I think the same thing happens
    on server-side, the secret key transaction should be secured. i.e. it
    should be protected with SSL for example.

    Security Consideration:
        You should make any secret keys encrypted. For example, AES256 would
        be a good idea. Note that you should NOT create your own encryption
        algorithm. Creating encryption algorithm requires super deep knowledge
        of mathematic skills and you are not a crypto-master.
    """

    widget = OTPSecretKeyWidget()

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.

        Keyword Arguments:
            qrcode_url: The url that generates qrcode.
            *args: Any arguments to be passed to self.__init__.
            **kwargs: Any keyword arguments to be passed to self.__init__.
        """
        qrcode_url = kwargs.pop("qrcode_url", None)
        render_kw = kwargs.pop("render_kw", {})
        if qrcode_url:
            render_kw["qrcode_url"] = qrcode_url
        super(OTPSecretKeyField, self).__init__(
            render_kw=render_kw, *args, **kwargs
        )

    def generate(self, **kwargs):
        """
        Generate Secret Key.

        Parameters:
            **kwargs: Optional. Any keyword arguments to be passed to
            `pyotp.random_base32`.

        Return Value: 16 chars random string that is able to be a secret key.

        """
        return random_base32(**kwargs)

    def qrcode(self, secret, **kwargs):
        """
        Generate the QRCode SVG image.

        This function returns SVG image that is able to be read by
        Google Authenticator or Authy.

        Parameters:
            **kwargs: Any keyword args to be passed to pyotp.utils.build_uri.

        """
        result = bytes()
        with BytesIO() as stream:
            generate_qrcode(
                build_otp_uri(secret, **kwargs), image_factory=svg
            ).save(stream)
            result = stream.getvalue()
        return result.decode("utf-8")

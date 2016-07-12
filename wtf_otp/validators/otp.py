#!/usr/bin/env python
# coding=utf-8

"""OTP Check Validator."""

from pyotp import TOTP
from wtforms.validators import ValidationError


class OTPCheck(object):
    """
    OTPCheck validator for WTForms.

    This validator checks whether input OTP is valid or not. If the input
    number is not correct, wtforms.validators.ValidationError is raised.
    """

    def __init__(self, secret, method="TOTP", call_args=None, **kwargs):
        """
        Initialize the validator.

        Parameters:
            secret: The secret key. This can be a callable function that
                returns the corresponding secret key.
            method: The method of otp. i.e. time-based otp or counter based
                otp. If you want to use time-based otp, set "TOTP". And,
                setting "HOTP", counter-based otp is used. Note that "TOTP" and
                "HOTP" is case-insensitive as the code shows.
            call_args: Any keyword arguments to be passed to
                pyotp.(TOTP|HTOP).verify(). Note that all values are able to
                be callable functions that return the corresponding values.
            **kwargs: Any keyword arguments to be passed to
                pyotp.(TOTP|HTOP).__init__(). Note that all values are able to
                be callable functions that return the corresponding values.
        """
        _method = method.lower()
        init_args = {}
        for (key, value) in kwargs.items():
            try:
                init_args[key] = value()
            except TypeError:
                init_args[key] = value

        self.call_args = call_args or {}
        if _method not in ["totp", "hotp"]:
            raise ValueError("The method should be \"totp\" or \"hotp\".")
        self.otp = TOTP(secret, **init_args)

    def __call__(self, form, field):
        """Validate the input data."""
        call_args = {}
        for (key, value) in self.call_args.items():
            try:
                call_args[key] = value()
            except TypeError:
                call_args[key] = value
        if not self.otp.verify(field.data, **call_args):
            raise ValidationError("OTP Token Mismatch.")

#!/usr/bin/env python
# coding=utf-8

"""OTP Check Validator."""

import pyotp
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
                This can be callable.
            call_args: Any keyword arguments to be passed to
                pyotp.(TOTP|HTOP).verify(). Note that all values are able to
                be callable functions that return the corresponding values.
            **kwargs: Any keyword arguments to be passed to
                pyotp.(TOTP|HTOP).__init__(). Note that all values are able to
                be callable functions that return the corresponding values.

        Note when putting callable value to each param:
            As you can see, all parameters can be callable function and when
            putitng it to each param, the value is evaluated dynamically.
            However, the form and field is passed as a parameter to the target
            variable. For example, if you put (lambda: "HOTP") to method param,
            the param is called with form, field. i.e. seld.method(form, field)
            as the code shows

        """
        self.method = method
        if isinstance(self.method, str):
            self.__check_method(self.method)
        self.secret = secret
        self.init_args = kwargs

        self.call_args = call_args or {}

    def __expand(self, value, form, field):
        try:
            return value(form, field)
        except TypeError:
            return value

    def __expand_dict(self, dct, form, field):
        expanded = {
            key: self.__expand(value, form, field)
            for (key, value) in dct.items()
        }
        return expanded

    def __check_method(self, value):
        if value not in ["TOTP", "HOTP"]:
            raise ValueError("The method should be \"totp\" or \"hotp\".")

    def __expand_method(self, form, field):
        ret = self.__expand(self.method, form, field).upper()
        self.__check_method(ret)
        return ret

    def __expand_init_args(self, form, field):
        return self.__expand_dict(self.init_args, form, field)

    def __expand_call_args(self, form, field):
        return self.__expand_dict(self.call_args, form, field)

    def __call__(self, form, field):
        """Validate the input data."""
        call_args = self.__expand_call_args(form, field)
        self.otp = getattr(pyotp, self.__expand_method(form, field))(
            self.__expand(self.secret, form, field),
            **self.__expand_init_args(form, field)
        )
        if not self.otp.verify(int(field.data), **call_args):
            raise ValidationError("OTP Token Mismatch.")

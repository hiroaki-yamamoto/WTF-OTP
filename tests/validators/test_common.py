#!/usr/bin/env python
# coding=utf-8

"""OTP Validation common error check."""

from unittest import TestCase

from wtforms.form import Form
import wtforms.fields as fld
from wtf_otp import OTPCheck


class OTPInitErrorTest(TestCase):
    """OTPCheck.__init__ error check when invalid value is put."""

    def test_invalid_value(self):
        """OTPCheck.__init__ should raise ValueError."""
        with self.assertRaises(ValueError) as e:
            class TestForm(Form):
                """Test Form."""

                totp = fld.StringField(validators=[
                    OTPCheck("base32secret", method="aloha")
                ])
        self.assertEqual(
            str(e.exception),
            "The method should be \"totp\" or \"hotp\"."
        )

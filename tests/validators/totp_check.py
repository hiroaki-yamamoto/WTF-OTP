#!/usr/bin/env python
# coding=utf-8

"""OTP validation tests."""

from unittest import TestCase

try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from pyotp import TOTP, random_base32
from wtforms import Form
from wtforms.fields import StringField
from wtf_otp import OTPCheck


class TOTPInitErrorTest(TestCase):
    """OTPCheck.__init__ error check when invalid value is put."""

    def test_invalid_value(self):
        """OTPCheck.__init__ should raise ValueError."""
        with self.assertRaises(ValueError) as e:
            class TestForm(Form):
                """Test Form."""

                totp = StringField(validators=[
                    OTPCheck("base32secret", method="aloha")
                ])
        self.assertEqual(
            str(e.exception),
            "The method should be \"totp\" or \"hotp\"."
        )


class TOTPNormalTest(TestCase):
    """Time-Based OTP Normal Situation Test."""

    @patch("wtf_otp.validators.otp.TOTP")
    def setUp(self, totp):
        """Setup."""
        self.secret = random_base32()
        self.totp = totp

        class TestForm(Form):
            """Test Form."""

            totp = StringField(validators=[
                OTPCheck(
                    self.secret, method="TOTP", interval=30,
                    call_args={"valid_window": 0}
                )
            ])

        self.key = TOTP(self.secret).now()
        self.form = TestForm(data={"totp": self.key})

    def test_init(self):
        """pyotp.TOTP() should be called."""
        self.totp.assert_called_once_with(self.secret, interval=30)

    def test_verify_check(self):
        """pyotp.TOTP().verify should be called."""
        self.totp.return_value.verify.assert_not_called()
        self.form.validate()
        self.totp.return_value.verify.assert_called_once_with(
            self.form.totp.data, valid_window=0
        )


class TOTPCallableTest(TestCase):
    """Time-Based OTP callable parameters Test."""

    @patch("wtf_otp.validators.otp.TOTP")
    def setUp(self, totp):
        """Setup."""
        self.secret = random_base32()
        self.totp = totp
        self.interval = MagicMock(return_value=30)
        self.valid_window = MagicMock(return_value=0)

        class TestForm(Form):
            """Test Form."""

            totp = StringField(validators=[
                OTPCheck(
                    self.secret, method="TOTP", interval=self.interval,
                    call_args={"valid_window": self.valid_window}
                )
            ])

        self.key = TOTP(self.secret).now()
        self.form = TestForm(data={"totp": self.key})

    def test_interval_call(self):
        """Interval that is set as init args should be called."""
        self.interval.assert_called_once_with()

    def test_init(self):
        """pyotp.TOTP() should be called."""
        self.totp.assert_called_once_with(
            self.secret, interval=self.interval.return_value
        )

    def test_verify_check(self):
        """pyotp.TOTP().verify should be called."""
        self.totp.return_value.verify.assert_not_called()
        self.valid_window.assert_not_called()
        self.form.validate()
        self.valid_window.assert_called_once_with()
        self.totp.return_value.verify.assert_called_once_with(
            self.form.totp.data, valid_window=self.valid_window.return_value
        )


class TOTPValidationErrorTest(TestCase):
    """Time-Based OTP Normal Situation Test."""

    @patch("wtf_otp.validators.otp.TOTP")
    def setUp(self, totp):
        """Setup."""
        self.secret = random_base32()
        self.totp = totp
        self.totp.return_value.verify.return_value = False

        class TestForm(Form):
            """Test Form."""

            totp = StringField(validators=[
                OTPCheck(
                    self.secret, method="TOTP", interval=30,
                    call_args={"valid_window": 0}
                )
            ])

        self.key = TOTP(self.secret).now()
        self.form = TestForm(data={"totp": self.key})

    def test_init(self):
        """pyotp.TOTP() should be called."""
        self.totp.assert_called_once_with(self.secret, interval=30)

    def test_verify_check(self):
        """pyotp.TOTP().verify should be called and has a error."""
        self.totp.return_value.verify.assert_not_called()
        self.form.validate()
        self.totp.return_value.verify.assert_called_once_with(
            self.form.totp.data, valid_window=0
        )
        self.assertDictEqual(
            {"totp": ["OTP Token Mismatch."]}, self.form.errors
        )

#!/usr/bin/env python
# coding=utf-8

"""HOTP validation tests."""

from unittest import TestCase
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from pyotp import random_base32, HOTP
from wtforms.form import Form
from wtforms.fields import StringField
from wtf_otp import OTPCheck


class HOTPNormalTest(TestCase):
    """Counter-Based OTP Normal Situation Test."""

    @patch("pyotp.HOTP")
    def setUp(self, hotp):
        """Setup."""
        self.secret = random_base32()
        self.hotp = hotp

        class TestForm(Form):
            """Test Form."""

            # Note that `window` parameter is just for testing.
            hotp = StringField(validators=[
                OTPCheck(
                    self.secret, method="HOTP", window=3,
                    call_args={"counter": 0}
                )
            ])

        self.key = HOTP(self.secret).at(0)
        self.form = TestForm(data={"hotp": self.key})

    def test_init(self):
        """pyotp.HOTP() should be called."""
        self.hotp.assert_called_once_with(self.secret, window=3)

    def test_verify_check(self):
        """pyotp.hOTP().verify should be called."""
        self.hotp.return_value.verify.assert_not_called()
        self.form.validate()
        self.hotp.return_value.verify.assert_called_once_with(
            self.form.hotp.data, counter=0
        )


class HOTPCallableTest(TestCase):
    """Counter-Based OTP callable parameters Test."""

    @patch("pyotp.HOTP")
    def setUp(self, hotp):
        """Setup."""
        self.secret = random_base32()
        self.hotp = hotp
        self.window = MagicMock(return_value=3)
        self.counter = MagicMock(return_value=0)

        class TestForm(Form):
            """Test Form."""

            # Note that `window` parameter is just for testing.
            hotp = StringField(validators=[
                OTPCheck(
                    self.secret, method="HOTP", window=self.window,
                    call_args={"counter": self.counter}
                )
            ])

        self.key = HOTP(self.secret).at(self.counter.return_value)
        self.form = TestForm(data={"hotp": self.key})

    def test_window_call(self):
        """Window that is set as init args should be called."""
        self.window.assert_called_once_with()

    def test_init(self):
        """pyotp.HOTP() should be called."""
        self.hotp.assert_called_once_with(
            self.secret, window=self.window.return_value
        )

    def test_verify_check(self):
        """pyotp.HOTP().verify should be called."""
        self.hotp.return_value.verify.assert_not_called()
        self.counter.assert_not_called()
        self.form.validate()
        self.counter.assert_called_once_with()
        self.hotp.return_value.verify.assert_called_once_with(
            self.form.hotp.data, counter=self.counter.return_value
        )


class HOTPValidationErrorTest(TestCase):
    """Counter-Based OTP Normal Situation Test."""

    @patch("pyotp.HOTP")
    def setUp(self, hotp):
        """Setup."""
        self.secret = random_base32()
        self.hotp = hotp
        self.hotp.return_value.verify.return_value = False

        class TestForm(Form):
            """Test Form."""

            # Note that `window` parameter is just for testing.
            hotp = StringField(validators=[
                OTPCheck(
                    self.secret, method="HOTP", window=3,
                    call_args={"counter": 0}
                )
            ])

        self.key = HOTP(self.secret).at(0)
        self.form = TestForm(data={"hotp": self.key})

    def test_init(self):
        """pyotp.HOTP() should be called."""
        self.hotp.assert_called_once_with(self.secret, window=3)

    def test_verify_check(self):
        """pyotp.HOTP().verify should be called and has a error."""
        self.hotp.return_value.verify.assert_not_called()
        self.form.validate()
        self.hotp.return_value.verify.assert_called_once_with(
            self.form.hotp.data, counter=0
        )
        self.assertDictEqual(
            {"hotp": ["OTP Token Mismatch."]}, self.form.errors
        )

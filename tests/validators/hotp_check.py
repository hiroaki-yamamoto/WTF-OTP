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

    def setUp(self):
        """Setup."""
        self.secret = random_base32()

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

    @patch("pyotp.HOTP")
    def test_init(self, hotp):
        """Any function shouldn't be called at this step."""
        hotp.assert_not_called
        hotp.return_value.verify.assert_not_called()

    @patch("pyotp.HOTP")
    def test_verify_check(self, hotp):
        """Verification step should be processed."""
        self.form.validate()
        hotp.assert_called_once_with(self.secret, window=3)
        hotp.return_value.verify.assert_called_once_with(
            int(self.form.hotp.data), counter=0
        )


class HOTPCallableTest(TestCase):
    """Counter-Based OTP callable parameters Test."""

    def setUp(self):
        """Setup."""
        self.secret = MagicMock(return_value=random_base32())
        self.window = MagicMock(return_value=3)
        self.counter = MagicMock(return_value=0)
        self.method = MagicMock(return_value="HOTP")

        class TestForm(Form):
            """Test Form."""

            # Note that `window` parameter is just for testing.
            hotp = StringField(validators=[
                OTPCheck(
                    self.secret, method=self.method, window=self.window,
                    call_args={"counter": self.counter}
                )
            ])

        self.key = HOTP(
            self.secret.return_value
        ).at(self.counter.return_value)
        self.form = TestForm(data={"hotp": self.key})

    @patch("pyotp.HOTP")
    def test_init(self, hotp):
        """Any funciton shouldn't be called at this time."""
        self.secret.assert_not_called()
        self.window.assert_not_called()
        hotp.assert_not_called()
        hotp.return_value.verify.assert_not_called()
        self.counter.assert_not_called()
        self.method.assert_not_called()

    @patch("pyotp.HOTP")
    def test_verify_check(self, hotp):
        """pyotp.HOTP().verify should be called."""
        self.form.validate()
        self.window.assert_called_once_with(self.form, self.form.hotp)
        self.secret.assert_called_once_with(self.form, self.form.hotp)
        self.counter.assert_called_once_with(self.form, self.form.hotp)
        self.method.assert_called_once_with(self.form, self.form.hotp)
        hotp.assert_called_once_with(
            self.secret.return_value, window=self.window.return_value
        )
        hotp.return_value.verify.assert_called_once_with(
            int(self.form.hotp.data), counter=self.counter.return_value
        )


class HOTPValidationErrorTest(TestCase):
    """Counter-Based OTP Normal Situation Test."""

    def setUp(self):
        """Setup."""
        self.secret = random_base32()

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

    @patch("pyotp.HOTP")
    def test_init(self, hotp):
        """Any function shouldn't be called at this time."""
        hotp.assert_not_called()
        hotp.return_value.verify.assert_not_called()

    @patch("pyotp.HOTP")
    def test_verify_check(self, hotp):
        """It should raise an error."""
        hotp.return_value.verify.return_value = False
        self.form.validate()
        hotp.assert_called_once_with(self.secret, window=3)
        hotp.return_value.verify.assert_called_once_with(
            int(self.form.hotp.data), counter=0
        )
        self.assertDictEqual(
            {"hotp": ["OTP Token Mismatch."]}, self.form.errors
        )

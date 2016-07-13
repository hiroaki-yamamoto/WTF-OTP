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


class TOTPNormalTest(TestCase):
    """Time-Based OTP Normal Situation Test."""

    def setUp(self):
        """Setup."""
        self.secret = random_base32()

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

    @patch("pyotp.TOTP")
    def test_init(self, totp):
        """Any arguments shouldn't be called at this step."""
        totp.assert_not_called()
        totp.return_value.verify.assert_not_called()

    @patch("pyotp.TOTP")
    def test_verify_check(self, totp):
        """Verification step should be processed."""
        self.form.validate()
        totp.assert_called_once_with(self.secret, interval=30)
        totp.return_value.verify.assert_called_once_with(
            int(self.form.totp.data), valid_window=0
        )


class TOTPCallableTest(TestCase):
    """Time-Based OTP callable parameters Test."""

    def setUp(self):
        """Setup."""
        self.secret = MagicMock(return_value=random_base32())
        self.interval = MagicMock(return_value=30)
        self.valid_window = MagicMock(return_value=0)
        self.method = MagicMock(return_value="TOTP")

        class TestForm(Form):
            """Test Form."""

            totp = StringField(validators=[
                OTPCheck(
                    self.secret, method=self.method, interval=self.interval,
                    call_args={"valid_window": self.valid_window}
                )
            ])

        self.key = TOTP(self.secret.return_value).now()
        self.form = TestForm(data={"totp": self.key})

    @patch("pyotp.TOTP")
    def test_init(self, totp):
        """Any functions shouldn't be called."""
        self.secret.assert_not_called()
        self.interval.assert_not_called()
        totp.assert_not_called()
        totp.return_value.verify.assert_not_called()
        self.valid_window.assert_not_called()
        self.method.assert_not_called()

    @patch("pyotp.TOTP")
    def test_verify_check(self, totp):
        """Verification step should be processed."""
        self.form.validate()
        totp.assert_called_once_with(
            self.secret.return_value, interval=self.interval.return_value
        )
        self.method.assert_called_once_with(self.form, self.form.totp)
        self.secret.assert_called_once_with(self.form, self.form.totp)
        self.interval.assert_called_once_with(self.form, self.form.totp)
        self.valid_window.assert_called_once_with(self.form, self.form.totp)
        totp.return_value.verify.assert_called_once_with(
            int(self.form.totp.data),
            valid_window=self.valid_window.return_value
        )


class TOTPValidationErrorTest(TestCase):
    """Time-Based OTP Normal Situation Test."""

    def setUp(self):
        """Setup."""
        self.secret = random_base32()

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

    @patch("pyotp.TOTP")
    def test_init(self, totp):
        """pyotp.TOTP() should be called."""
        totp.assert_not_called()
        totp.return_value.verify.assert_not_called()

    @patch("pyotp.TOTP")
    def test_verify_check(self, totp):
        """It should raise a error."""
        totp.return_value.verify.return_value = False
        self.form.validate()
        totp.assert_called_once_with(self.secret, interval=30)
        totp.return_value.verify.assert_called_once_with(
            int(self.form.totp.data), valid_window=0
        )
        self.assertDictEqual(
            {"totp": ["OTP Token Mismatch."]}, self.form.errors
        )

#!/usr/bin/env python
# coding=utf-8

"""OTP Secret Field Tests."""

import re
from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from wtforms.form import Form

from wtf_otp import OTPSecretKeyWidget, OTPSecretKeyField


class TestForm(Form):
    """Test Form."""

    otp = OTPSecretKeyField()


class FieldTestBase(TestCase):
    """Secret field test base class."""

    def setUp(self):
        """Setup function."""
        self.TestForm = TestForm
        self.form = self.TestForm()


class SecretFieldTest(FieldTestBase):
    """Secret field Normal Initialization Test."""

    def test_widget_type(self):
        """The widget should be an instance of OTPSecretKeyWidget."""
        self.assertIsInstance(self.form.otp.widget, OTPSecretKeyWidget)


class SecretFieldGenerationTest(FieldTestBase):
    """Secret field secret key generation test."""

    def test_secret_generation(self):
        """QRCode should be generated."""
        self.assertRegexpMatches(
            self.form.otp.generate(), re.compile("^[A-Z,2-7]{16}$")
        )

    @patch("wtf_otp.fields.secret_key.random_base32")
    def test_secret_param(self, generation):
        """QRCode should be generated."""
        test = {
            ("test{}").format(num): ("test_test{}").format(num)
            for num in range(20)
        }
        self.form.otp.generate(**test)
        generation.assert_called_once_with(**test)

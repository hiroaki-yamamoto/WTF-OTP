#!/usr/bin/env python
# coding=utf-8

"""OTP Secret Field Tests."""


from unittest import TestCase

from wtforms.form import Form

from wtf_otp import OTPSecretKeyWidget, OTPSecretKeyField


class SecretFieldNormalInitTest(TestCase):
    """Secret field Normal Initialization Test."""

    def setUp(self):
        """Setup function."""
        class TestForm(Form):
            otp = OTPSecretKeyField()

        self.TestForm = TestForm
        self.form = self.TestForm()

    def test_widget_type(self):
        """The widget should be an instance of OTPSecretKeyWidget."""
        self.assertIsInstance(self.form.otp.widget, OTPSecretKeyWidget)

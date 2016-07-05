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


class SecretFieldQRCodeGenerationTest(FieldTestBase):
    """Secret field qrcode generation test."""

    @patch("wtf_otp.fields.secret_key.build_otp_uri")
    @patch("wtf_otp.fields.secret_key.generate_qrcode")
    def setUp(self, qrcode_mock, otpurl):
        """Setup."""
        super(SecretFieldQRCodeGenerationTest, self).setUp()
        self.otpurl = otpurl
        self.qrcode_mock = qrcode_mock
        self.secret = self.form.otp.generate()
        self.param = {
            "name": "test@example.com",
            "issuer_name": "Test Issuer"
        }
        self.otpurl.return_value = \
            ("otpauth://totp/Test Issuer:test@example.com?secret={}").format(
                self.secret
            )
        self.qr_code = self.form.otp.qrcode(
            self.secret, **self.param
        )

    def test_param(self):
        """The arguments should be passed to the otpurl as-is."""
        self.otpurl.assert_called_once_with(self.secret, **self.param)

    # def test_filetype(self):
    #     """The text type should be svg."""
    #     from xml.etree import ElementTree
    #     self.assertEqual(
    #         ElementTree.fromstring(self.qr_code).tag,
    #         "{http://www.w3.org/2000/svg}svg",
    #         "The generated text is not SVG format."
    #     )

    def test_qrcode_body(self):
        """QRCode Generator should be called with proper args."""
        from qrcode.image.svg import SvgImage as svg
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        self.qrcode_mock.assert_called_once_with(
            quote(self.otpurl.return_value, "!@:/?="),
            image_factory=svg
        )

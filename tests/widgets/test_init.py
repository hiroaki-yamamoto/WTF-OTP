#!/usr/bin/env python
# coding=utf-8

"""OTP Widget Tests."""

from unittest import TestCase
from wtforms.widgets import HTMLString, html_params
from wtf_otp import OTPWidget
from wtf_otp.templates import jquery_template


class OTPWidgetNormalInitTest(TestCase):
    """Normal Initialization Tests."""

    def setUp(self):
        """Setup."""
        self.field = type("OTPTestField", (object, ), {
            "name": "test",
            "id": "testid"
        })
        self.widget = OTPWidget()
        self.expected = HTMLString(
            "<input type=\"text\" readonly {}>"
            "<button type=\"button\" {}>Get Secret Key</button>{}"
        ).format(
            html_params(id=self.field.id, name=self.field.name),
            html_params(id="btn-" + self.field.id),
            jquery_template.render(
                btnid="btn-" + self.field.id, inputid=self.field.id
            )
        )

    def test_call(self):
        """The widget should generate jquery based widget."""
        result = self.widget(self.field)
        self.assertEqual(result, self.expected)

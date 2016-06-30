#!/usr/bin/env python
# coding=utf-8

"""OTP Widget Tests."""

from unittest import TestCase
from wtforms.widgets import HTMLString, html_params
from wtf_otp import OTPSecretKeyWidget
from wtf_otp.templates import jquery_template, angular_template


class OTPTestField(object):
    """OTPTestField."""

    def __init__(self):
        """Init the function."""
        self.name = "test"
        self.id = "testid"
        self.render_kw = {}


class OTPWidgetNormalInitTest(TestCase):
    """Normal Initialization Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.widget = OTPSecretKeyWidget()
        self.expected = HTMLString(
            "<input type=\"text\" readonly {}>"
            "<button type=\"button\" {}>Get Secret Key</button>{}"
        ).format(
            html_params(id=self.field.id, name=self.field.name),
            html_params(id="btn-" + self.field.id),
            jquery_template.render(
                btnid=("btn-{}").format(self.field.id), inputid=self.field.id
            )
        )

    def test_call(self):
        """The widget should generate jquery based widget."""
        result = self.widget(self.field)
        self.assertEqual(result, self.expected)


class OTPWidgetAngularInitTest(TestCase):
    """AngularJS based initialization test."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {"data-ng-model": "test.data"}
        self.widget = OTPSecretKeyWidget()
        self.expected = HTMLString(
            "<input type=\"text\" readonly {}>"
            "<button type=\"button\" {}>Get Secret Key</button>{}"
        ).format(
            html_params(
                id=self.field.id, name=self.field.name,
                **self.field.render_kw
            ),
            html_params(id="btn-" + self.field.id, **{
                "data-ng-click": ("click{}()").format(id(self.field))
            }),
            angular_template.render(
                fieldid=id(self.field), inputid=self.field.id,
                ng_model=self.field.render_kw["data-ng-model"]
            )
        )

    def test_call(self):
        """The widget should generate AngularJS based view."""
        result = self.widget(self.field, **self.field.render_kw)
        self.assertEqual(result, self.expected)

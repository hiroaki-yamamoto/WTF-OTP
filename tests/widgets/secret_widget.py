#!/usr/bin/env python
# coding=utf-8

"""OTP Secret Ket Widget Tests."""

from unittest import TestCase
from wtforms.widgets import HTMLString, html_params
from wtf_otp import OTPSecretKeyWidget
from wtf_otp.widgets.templates import jquery_template, angular_template


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
            "<div {}>"
            "<input type=\"text\" readonly {}>"
            "<button type=\"button\" {}>Get Secret Key</button>{}"
            "</div>"
        ).format(
            html_params(**{"class": "form-group"}),
            html_params(id=self.field.id, name=self.field.name),
            html_params(id="btn-" + self.field.id),
            jquery_template.render(
                btnid=("btn-{}").format(self.field.id), inputid=self.field.id
            )
        )

    def test_call(self):
        """The widget should generate jquery based widget."""
        result = self.widget(self.field, div_args={"class": "form-group"})
        self.assertEqual(result, self.expected)


class OTPWidgetAngularInitTest(TestCase):
    """AngularJS based initialization test."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {"data-ng-model": "test.data"}
        self.widget = OTPSecretKeyWidget()
        self.expected = HTMLString(
            "<div {}>"
            "<input type=\"text\" readonly {}>"
            "<button type=\"button\" {}>Get Secret Key</button>{}"
            "</div>"
        ).format(
            html_params(**{
                "class": "form-group",
                "data-ng-controller": ("OTP{}Controller").format(
                    id(self.field)
                )
            }),
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
        result = self.widget(
            self.field, div_args={"class": "form-group"},
            **self.field.render_kw
        )
        self.assertEqual(result, self.expected)


class OTPWidgetJQueryQRCodeTest(TestCase):
    """JQuery QR-code Generation Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.widget = OTPSecretKeyWidget()
        self.expected = HTMLString(
            "<div {}>"
            "<img id=\"otpauthQR{}\">"
            "<input type=\"text\" readonly {}>"
            "<button type=\"button\" {}>Get Secret Key</button>{}"
            "</div>"
        ).format(
            html_params(**{"class": "form-group"}),
            self.field.id,
            html_params(id=self.field.id, name=self.field.name),
            html_params(id="btn-" + self.field.id),
            jquery_template.render(
                btnid=("btn-{}").format(self.field.id), inputid=self.field.id,
                qrcode_url="/qrcode"
            )
        )

    def test_call(self):
        """The widget should generate jquery based widget with qrcode."""
        result = self.widget(
            self.field, div_args={"class": "form-group"},
            qrcode_url="/qrcode"
        )
        self.assertEqual(result, self.expected)

#!/usr/bin/env python
# coding=utf-8

"""OTP Secret Ket Widget Tests."""

from unittest import TestCase
from jinja2 import Markup
from wtf_otp import OTPSecretKeyWidget


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
        self.expected = Markup(
            self.widget.templates.get_template("widget.html").render(
                div_args={"class": "form-group"},
                input_args=dict(
                    id=self.field.id, name=self.field.name,
                    **self.field.render_kw
                ),
                button_args={"id": "btn-" + self.field.id}
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
        self.expected = Markup(
            self.widget.templates.get_template("widget.html").render(
                div_args={
                    "class": "form-group",
                    "data-ng-controller": (
                        "OTP{}Controller"
                    ).format(id(self.field))
                },
                input_args=dict(
                    id=self.field.id, name=self.field.name,
                    **self.field.render_kw
                ),
                button_args={
                    "id": "btn-" + self.field.id,
                    "data-ng-click": ("click{}()").format(id(self.field))
                },
                script_args={
                    "module": "testModule",
                    "fieldid": id(self.field),
                    "inputid": self.field.id,
                    "ng_model": self.field.render_kw["data-ng-model"]
                }
            )
        )

    def test_call(self):
        """The widget should generate AngularJS based view."""
        result = self.widget(
            self.field, module="testModule",
            div_args={"class": "form-group"},
            **self.field.render_kw
        )
        self.assertEqual(result, self.expected)


class OTPWidgetJQueryQRCodeTest(TestCase):
    """JQuery QR-code Generation Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.widget = OTPSecretKeyWidget()
        self.expected = Markup(
            self.widget.templates.get_template("widget.html").render(
                div_args={"class": "form-group"},
                input_args=dict(
                    id=self.field.id, name=self.field.name,
                    **self.field.render_kw
                ),
                button_args={"id": "btn-" + self.field.id},
                qrcode="/qrcode",
                qrcode_args={"id": ("otpauthQR{}").format(self.field.id)}
            )
        )

    def test_call(self):
        """The widget should generate jquery based widget with qrcode."""
        result = self.widget(
            self.field, div_args={"class": "form-group"},
            qrcode_url="/qrcode"
        )
        self.assertEqual(result, self.expected)


class OTPWidgetAngularQRCodeTest(TestCase):
    """Angular QR-code Generation Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {
            "data-ng-model": "test.data"
        }
        self.widget = OTPSecretKeyWidget()
        self.expected = Markup(
            self.widget.templates.get_template("widget.html").render(
                div_args={
                    "class": "form-group",
                    "data-ng-controller": (
                        "OTP{}Controller"
                    ).format(id(self.field))
                },
                input_args=dict(
                    id=self.field.id, name=self.field.name,
                    **self.field.render_kw
                ),
                button_args={
                    "id": "btn-" + self.field.id,
                    "data-ng-click": ("click{}()").format(id(self.field))
                },
                script_args={
                    "module": "testModule",
                    "fieldid": id(self.field),
                    "inputid": self.field.id,
                    "ng_model": self.field.render_kw["data-ng-model"]
                },
                qrcode="/qrcode",
                qrcode_args={
                    "id": ("otpauthQR{}").format(self.field.id),
                    "data-ng-style": "qrcodeStyle"
                }
            )
        )

    def test_call(self):
        """The widget should generate angularjs based widget with qrcode."""
        result = self.widget(
            self.field, div_args={"class": "form-group"},
            module="testModule", qrcode_url="/qrcode",
            **self.field.render_kw
        )
        print(result)
        print(self.expected)
        self.assertEqual(result, self.expected)

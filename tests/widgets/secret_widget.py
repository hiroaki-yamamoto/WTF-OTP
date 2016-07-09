#!/usr/bin/env python
# coding=utf-8

"""OTP Secret Ket Widget Tests."""

from unittest import TestCase
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
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
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate jquery based widget."""
        self.widget(self.field, div_args={"class": "form-group"})
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with(
            "widget.html"
        )
        get_template.return_value.render.assert_called_once_with(
            div_args={"class": "form-group"},
            input_args=dict(
                id=self.field.id, name=self.field.name,
                **self.field.render_kw
            ),
            button_args={"id": "btn-" + self.field.id},
            qrcode={},
            script_args={}
        )


class OTPWidgetAngularInitTest(TestCase):
    """AngularJS based initialization test."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {"data-ng-model": "test.data"}
        self.widget = OTPSecretKeyWidget()
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate AngularJS based view."""
        self.widget(
            self.field, module="testModule",
            div_args={"class": "form-group"},
            **self.field.render_kw
        )
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
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
                "ng_model": self.field.render_kw["data-ng-model"]
            },
            qrcode={}
        )

    def test_module_exception(self):
        """Should show ValueError to tell module name is missing."""
        with self.assertRaises(ValueError) as err:
            self.widget(
                self.field,
                div_args={"class": "form-group"},
                **self.field.render_kw
            )
        self.assertEqual(
            str(err.exception),
            "AngularJS module name is needed to use AngularJS."
        )


class OTPWidgetJQueryQRCodeTest(TestCase):
    """JQuery QR-code Generation Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.widget = OTPSecretKeyWidget()
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate jquery based widget with qrcode."""
        self.widget(
            self.field, div_args={"class": "form-group"},
            qrcode_url="/qrcode"
        )
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
            div_args={"class": "form-group"},
            input_args=dict(
                id=self.field.id, name=self.field.name,
                **self.field.render_kw
            ),
            button_args={"id": "btn-" + self.field.id},
            qrcode={
                "url": "/qrcode",
                "args": {"id": ("otpauthQR{}").format(self.field.id)}
            },
            script_args={}
        )


class OTPWidgetAngularQRCodeTest(TestCase):
    """Angular QR-code Generation Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {
            "data-ng-model": "test.data"
        }
        self.widget = OTPSecretKeyWidget()
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate angularjs based widget with qrcode."""
        self.widget(
            self.field, div_args={"class": "form-group"},
            module="testModule", qrcode_url="/qrcode",
            **self.field.render_kw
        )
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
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
                "ng_model": self.field.render_kw["data-ng-model"]
            },
            qrcode={
                "url": "/qrcode",
                "args": {
                    "id": ("otpauthQR{}").format(self.field.id),
                    "data-ng-style": "qrcodeStyle"
                }
            }
        )

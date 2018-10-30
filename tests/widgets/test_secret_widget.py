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
        get_template.assert_called_once_with("widget.html")
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


class OTPWidgetContainsDataTest(TestCase):
    """Normal initlaization, but it contains data."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.data = "test"
        self.widget = OTPSecretKeyWidget()
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate jquery based widget with the value."""
        self.widget(self.field, div_args={"class": "form-group"})
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
            div_args={"class": "form-group"},
            input_args=dict(
                id=self.field.id, name=self.field.name,
                value=self.field.data, **self.field.render_kw
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
            self.field, div_args={"class": "form-group"},
            **self.field.render_kw
        )
        ngmodel = self.field.render_kw.pop("data-ng-model")
        self.field.render_kw["data-ng-model"] = "ngModel"
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
            div_args={
                "class": "form-group",
                ("data-otp-field{}").format(id(self.field)): True,
                "data-ng-model": ngmodel
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
                "fieldid": id(self.field)
            },
            qrcode={}
        )


class OTPAngularWidgetContainsDataTest(TestCase):
    """Normal initlaization, but it contains data."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {"data-ng-model": "test.data"}
        self.field.data = "test"
        self.widget = OTPSecretKeyWidget()
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate angular based widget with the value."""
        self.widget(
            self.field, div_args={"class": "form-group"},
            **self.field.render_kw
        )
        ngmodel = self.field.render_kw.pop("data-ng-model")
        self.field.render_kw["data-ng-model"] = "ngModel"
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
            div_args={
                "class": "form-group",
                ("data-otp-field{}").format(id(self.field)): True,
                "data-ng-model": ngmodel
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
                "fieldid": id(self.field),
                "data": self.field.data
            },
            qrcode={}
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
                "args": {
                    "id": ("otpauthQR{}").format(self.field.id),
                    "class": "otp-qrcode"
                }
            },
            script_args={}
        )


class OTPWidgetAngularQRCodeTest(TestCase):
    """Angular QR-code Generation Tests."""

    def setUp(self):
        """Setup."""
        self.field = OTPTestField()
        self.field.render_kw = {
            "data-ng-model": "model.test"
        }
        self.widget = OTPSecretKeyWidget()
        self.widget.templates.get_template = MagicMock()

    def test_call(self):
        """The widget should generate angularjs based widget with qrcode."""
        self.widget(
            self.field, div_args={"class": "form-group"},
            qrcode_url="/qrcode", **self.field.render_kw
        )
        ngmodel = self.field.render_kw.pop("data-ng-model")
        self.field.render_kw["data-ng-model"] = "ngModel"
        get_template = self.widget.templates.get_template
        get_template.assert_called_once_with("widget.html")
        get_template.return_value.render.assert_called_once_with(
            div_args={
                "class": "form-group",
                ("data-otp-field{}").format(id(self.field)): True,
                "data-ng-model": ngmodel
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
                "fieldid": id(self.field)
            },
            qrcode={
                "url": "/qrcode",
                "args": {
                    "id": ("otpauthQR{}").format(self.field.id),
                    "class": "otp-qrcode"
                }
            }
        )

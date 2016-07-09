#!/usr/bin/env python
# coding=utf-8

"""OTP Widgets."""
from jinja2 import Environment, PackageLoader,  Markup


class OTPSecretKeyWidget(object):
    """
    OTP Widget.

    This widget readonly input, and "Get Secret Key" button.
    Clicking the "Generate" button, a new secret key is generated thru
    browser-side generator.
    """

    def __init__(self):
        """Initialize the widget."""
        self.templates = Environment(
            loader=PackageLoader("wtf_otp.widgets")
        )

    def __call__(self, field, **kwargs):
        """
        Generate OTPWidget.

        Parameters:
            **kwargs: Any arguments to be applied to input.
                If input_args has dict value, input_args.update(kwargs) is
                called after parameter transformation.
                Note that the values of button_args and div_args are applied
                to button and div. For details, refer keyword arguments.
        Keyword Arguments:
            input_args: Any arguments to be applied to input.
            button_args: Any arguments to be applied to button only.
            div_args: Any argument that to applied to div wrap.
                i.e. inputs are wrapped with div tags.
            module: The module name to be attached.
            qrcode_url: URL to generate QR Code.
                CAUTION: DO NOT specify external url for security reason.
        """
        input_args = kwargs.pop("input_args", {})
        button_args = kwargs.pop("button_args", {})
        div_args = kwargs.pop("div_args", {})
        qrcode = {}
        qrcode_url = kwargs.pop("qrcode_url", None)
        if qrcode_url:
            qrcode.update({
                "url": qrcode_url,
                "args": {"id": ("otpauthQR{}").format(field.id)}
            })
        module = kwargs.pop("module", None)
        script_args = {}

        input_args.update(kwargs)
        input_args.setdefault("id", field.id)
        input_args.setdefault("name", field.name)

        button_args.setdefault("id", "btn-" + field.id)
        # Because I strongly recommend to use data-* attribute for custom
        # attributes, angular aimed option is available only for data-*
        # attributes.
        if "data-ng-model" in input_args:
            if not module:
                raise ValueError(
                    "AngularJS module name is needed to use AngularJS."
                )
            button_args["data-ng-click"] = ("click{}()").format(id(field))
            div_args.update({
                "data-ng-app": ("OTP{}Module").format(id(field)),
                "data-ng-controller": ("OTP{}Controller").format(id(field))
            })
            if qrcode_url:
                qrcode["args"].update({"data-ng-style": "qrcodeStyle"})
            script_args.update({
                "module": module,
                "fieldid": id(field),
                "ng_model": input_args["data-ng-model"]
            })

        return Markup(self.templates.get_template("widget.html").render(
            input_args=input_args, script_args=script_args,
            qrcode=qrcode, button_args=button_args,
            div_args=div_args
        ))

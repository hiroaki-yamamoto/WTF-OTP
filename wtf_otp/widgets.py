#!/usr/bin/env python
# coding=utf-8

"""OTP Widgets."""
from wtforms.widgets import html_params, HTMLString

from .templates import jquery_template, angular_template


class OTPSecretKeyWidget(object):
    """
    OTP Widget.

    This widget includes QR-code, readonly input, and "Get Secret Key" button.
    Clicking the "Generate" button, a new secret key is generated thru
    browser-side generator. Changing secret key, the QR-code is also changed.
    """

    def __call__(self, field, otp_method="totp", input_args=None,
                 button_args=None, div_args=None, **kwargs):
        """
        Generate OTPWidget.

        Parameters:
            **kwargs: Alias of input_args. When input_args is also specified,
                this is merged to input_args.
                i.e. input_args.update(kwargs) is called.
        Keyword Arguments:
            otp_method: Set "totp" if you want to use time-based otp, or
                "hotp" if you want to use Counter-Based otp.
            input_args: Any arguments to be applied to readonly
                input only.
            button_args: Any arguments to be applied to button only.
            div_args: Any argument that to applied to div wrap.
                i.e. inputs are wrapped with div tags.
        """
        input_args = {} if not input_args else input_args
        button_args = {} if not button_args else button_args
        div_args = {} if not div_args else div_args

        input_args.update(kwargs)
        input_args.setdefault("id", field.id)
        input_args.setdefault("name", field.name)
        input_widget = HTMLString((
            "<input type=\"text\" readonly {}>"
        ).format(html_params(**input_args)))

        button_args.setdefault("id", "btn-" + field.id)
        # Because I strongly recommend to use data-* attribute for custom
        # attributes, angular aimed option is available only for data-*
        # attributes.
        if "data-ng-model" in input_args:
            button_args["data-ng-click"] = ("click{}()").format(id(field))
            div_args["data-ng-controller"] = ("OTP{}Controller").format(
                id(field)
            )
        button_widget = HTMLString((
            "<button type=\"button\" {}>Get Secret Key</button>"
        ).format(html_params(**button_args) if button_args else ""))
        div_widget = ("<div {}>").format(
            html_params(**div_args)
        ) if div_args else "<div>"
        script_widget = HTMLString(
            angular_template.render(
                fieldid=id(field), ng_model=input_args["data-ng-model"]
            ) if "data-ng-model" in input_args else jquery_template.render(
                btnid=button_args["id"], inputid=input_args["id"]
            )
        )
        return ("").join([
            div_widget, input_widget, button_widget, script_widget, "</div>"
        ])
